from __future__ import annotations

import secrets
import string
from datetime import datetime, timedelta
from pathlib import Path
from random import choice

from ad_console.config import Settings
from ad_console.domain.models import (
    AccountRequest,
    ChatMessage,
    DirectoryUser,
    EmailMessage,
    UnlockRequest,
    VerificationCode,
)
from ad_console.domain.ports import (
    AIChatPort,
    AccountRequestRepository,
    AutomationPort,
    DirectoryPort,
    EmailPort,
    IdentityVerifierPort,
    NotificationPort,
    UnlockRequestRepository,
    VerificationCodeRepository,
)


class AccountService:
    def __init__(
        self,
        repo: AccountRequestRepository,
        directory: DirectoryPort,
        notifier: NotificationPort,
    ) -> None:
        self._repo = repo
        self._directory = directory
        self._notifier = notifier

    def create_request(
        self, *, username: str, email: str, full_name: str, department: str, reason: str
    ) -> str:
        request_id = secrets.token_urlsafe(16)
        item = AccountRequest(
            request_id=request_id,
            username=username,
            email=email,
            full_name=full_name,
            department=department,
            reason=reason,
            created_at=datetime.now(),
        )
        self._repo.save(item)
        self._notifier.send(
            f"[Account Request]\nName: {full_name}\nDepartment: {department}\nEmail: {email}\nUsername: {username}\nReason: {reason}"
        )
        return request_id

    def approve(self, request_id: str) -> tuple[AccountRequest | None, str]:
        item = self._repo.get(request_id)
        if not item:
            return None, ""

        temp_password = _generate_password()
        self._directory.create_user(
            DirectoryUser(username=item.username, email=item.email, full_name=item.full_name),
            temp_password,
        )
        self._repo.delete(request_id)
        self._notifier.send(f"[Approved] {item.username} account created.")
        return item, temp_password

    def reject(self, request_id: str) -> AccountRequest | None:
        item = self._repo.get(request_id)
        if item:
            self._repo.delete(request_id)
            self._notifier.send(f"[Rejected] {item.username} account request rejected.")
        return item

    def list_pending(self) -> list[AccountRequest]:
        return self._repo.list_all()


class PasswordService:
    def __init__(
        self,
        verifier: IdentityVerifierPort,
        directory: DirectoryPort,
        codes: VerificationCodeRepository,
        emailer: EmailPort,
        settings: Settings,
    ) -> None:
        self._verifier = verifier
        self._directory = directory
        self._codes = codes
        self._emailer = emailer
        self._settings = settings

    def verify_current_password(self, username: str, password: str) -> bool:
        return self._verifier.verify_password(username, password)

    def change_password(self, username: str, current_password: str, new_password: str) -> bool:
        if not self._verifier.verify_password(username, current_password):
            return False
        self._directory.reset_password(username, new_password)
        return True

    def send_reset_code(self, username: str, email: str) -> None:
        code = str(secrets.randbelow(1000000)).zfill(6)
        self._codes.save(
            VerificationCode(
                username=username,
                email=email,
                code=code,
                expires_at=datetime.now() + timedelta(minutes=10),
            )
        )
        self._emailer.send(
            EmailMessage(
                to=email,
                subject=f"[{self._settings.service_name}] Password reset verification code",
                html=f"<h2>Password reset verification code</h2><p><strong>{code}</strong></p><p>This code is valid for 10 minutes.</p>",
            )
        )

    def reset_with_code(self, username: str, email: str, code: str) -> str | None:
        stored = self._codes.get(username)
        if not stored or stored.email != email or stored.code != code or datetime.now() > stored.expires_at:
            return None

        temp_password = _generate_password()
        self._directory.reset_password(username, temp_password)
        self._codes.delete(username)
        self._emailer.send(
            EmailMessage(
                to=email,
                subject=f"[{self._settings.service_name}] Temporary password issued",
                html=(
                    f"<h2>Temporary password</h2><p>User: <strong>{username}</strong></p>"
                    f"<p>Password: <strong>{temp_password}</strong></p>"
                ),
            )
        )
        return temp_password

    def admin_reset(self, username: str, email: str) -> str:
        temp_password = _generate_password()
        self._directory.reset_password(username, temp_password)
        self._emailer.send(
            EmailMessage(
                to=email,
                subject=f"[{self._settings.service_name}] Password reset complete",
                html=f"<h2>Password reset complete</h2><p>Temporary password: <strong>{temp_password}</strong></p>",
            )
        )
        return temp_password


class AccessSupportService:
    def __init__(
        self,
        repo: UnlockRequestRepository,
        notifier: NotificationPort,
        automation: AutomationPort,
        emailer: EmailPort,
        settings: Settings,
    ) -> None:
        self._repo = repo
        self._notifier = notifier
        self._automation = automation
        self._emailer = emailer
        self._settings = settings

    def request_unlock(self, username: str, email: str, reason: str) -> str:
        request_id = secrets.token_urlsafe(16)
        self._repo.save(
            UnlockRequest(
                request_id=request_id,
                username=username,
                email=email,
                reason=reason,
                created_at=datetime.now(),
            )
        )
        self._notifier.send(f"[Unlock Request]\nUsername: {username}\nEmail: {email}\nReason: {reason}")
        return request_id

    def approve_unlock(self, request_id: str) -> UnlockRequest | None:
        item = self._repo.get(request_id)
        if not item:
            return None
        self._repo.delete(request_id)
        self._automation.run_unlock(item.username, item.email)
        self._emailer.send(
            EmailMessage(
                to=item.email,
                subject=f"[{self._settings.service_name}] Account unlock completed",
                html=f"<h2>Account unlock completed</h2><p>User <strong>{item.username}</strong> can sign in again.</p>",
            )
        )
        self._notifier.send(f"[Unlock Approved] {item.username}")
        return item

    def reject_unlock(self, request_id: str) -> UnlockRequest | None:
        item = self._repo.get(request_id)
        if not item:
            return None
        self._repo.delete(request_id)
        self._emailer.send(
            EmailMessage(
                to=item.email,
                subject=f"[{self._settings.service_name}] Account unlock request rejected",
                html=f"<h2>Unlock request rejected</h2><p>Please contact {self._settings.support_email} for follow-up.</p>",
            )
        )
        self._notifier.send(f"[Unlock Rejected] {item.username}")
        return item

    def request_qr_reissue(self, username: str, email: str, reason: str) -> None:
        self._notifier.send(f"[VPN QR Reissue]\nUsername: {username}\nEmail: {email}\nReason: {reason}")


class AIChatService:
    def __init__(self, chat_adapter: AIChatPort, settings: Settings) -> None:
        self._chat_adapter = chat_adapter
        self._settings = settings

    def chat(self, raw_messages: list[dict[str, str]]) -> str:
        history = [ChatMessage(role=item.get("role", ""), text=item.get("text", "").strip()) for item in raw_messages]
        history = [item for item in history if item.text]
        if not history:
            raise ValueError("No messages provided.")
        return self._chat_adapter.reply(history, self._load_persona())

    def _load_persona(self) -> str:
        persona_path = Path(__file__).resolve().parents[2] / "docs" / "AI_PERSONA.md"
        if persona_path.exists():
            return persona_path.read_text(encoding="utf-8")
        return (
            f"You are a helpful assistant for {self._settings.service_name}. "
            "Give operational guidance, explain the next step clearly, and avoid exposing secrets."
        )


def _generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return "".join(choice(alphabet) for _ in range(length))
