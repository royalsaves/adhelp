from __future__ import annotations

from pathlib import Path

from flask import Flask
from flask_cors import CORS

from ad_console.adapters.ai import BedrockAIChatAdapter, DemoAIChatAdapter
from ad_console.adapters.automation import HttpAutomationAdapter, NullAutomationAdapter
from ad_console.adapters.directory import (
    AwsDirectoryAdapter,
    DemoDirectoryAdapter,
    DemoIdentityVerifier,
    LdapIdentityVerifier,
)
from ad_console.adapters.emailing import ConsoleEmailAdapter, SesEmailAdapter
from ad_console.adapters.notifications import NullNotificationAdapter, SlackNotificationAdapter
from ad_console.adapters.repositories import (
    InMemoryAccountRequestRepository,
    InMemoryUnlockRequestRepository,
    InMemoryVerificationCodeRepository,
)
from ad_console.api import build_api_blueprint
from ad_console.application.services import AIChatService, AccessSupportService, AccountService, PasswordService
from ad_console.config import Settings


def create_app() -> Flask:
    settings = Settings()
    static_folder = str(Path(__file__).resolve().parents[2] / "frontend" / "dist")
    app = Flask(__name__, static_folder=static_folder, static_url_path=None)
    CORS(app)

    account_repo = InMemoryAccountRequestRepository()
    unlock_repo = InMemoryUnlockRequestRepository()
    code_repo = InMemoryVerificationCodeRepository()

    if settings.app_mode == "demo":
        directory = DemoDirectoryAdapter()
        verifier = DemoIdentityVerifier()
        notifier = NullNotificationAdapter()
        emailer = ConsoleEmailAdapter()
        automation = NullAutomationAdapter()
        ai_adapter = DemoAIChatAdapter()
    else:
        directory = AwsDirectoryAdapter(settings)
        verifier = LdapIdentityVerifier(settings)
        notifier = (
            SlackNotificationAdapter(settings.slack_webhook_url)
            if settings.slack_webhook_url
            else NullNotificationAdapter()
        )
        emailer = SesEmailAdapter(settings)
        automation = HttpAutomationAdapter(settings.ansible_api_url, settings.ansible_token)
        ai_adapter = BedrockAIChatAdapter(settings)

    services = {
        "account_service": AccountService(account_repo, directory, notifier),
        "password_service": PasswordService(verifier, directory, code_repo, emailer, settings),
        "support_service": AccessSupportService(unlock_repo, notifier, automation, emailer, settings),
        "ai_service": AIChatService(ai_adapter, settings),
    }

    app.register_blueprint(build_api_blueprint(services, static_folder))
    return app
