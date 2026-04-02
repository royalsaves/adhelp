from __future__ import annotations

from ad_console.domain.models import AccountRequest, UnlockRequest, VerificationCode


class InMemoryAccountRequestRepository:
    def __init__(self) -> None:
        self._items: dict[str, AccountRequest] = {}

    def save(self, item: AccountRequest) -> None:
        self._items[item.request_id] = item

    def get(self, request_id: str) -> AccountRequest | None:
        return self._items.get(request_id)

    def delete(self, request_id: str) -> None:
        self._items.pop(request_id, None)

    def list_all(self) -> list[AccountRequest]:
        return list(self._items.values())


class InMemoryUnlockRequestRepository:
    def __init__(self) -> None:
        self._items: dict[str, UnlockRequest] = {}

    def save(self, item: UnlockRequest) -> None:
        self._items[item.request_id] = item

    def get(self, request_id: str) -> UnlockRequest | None:
        return self._items.get(request_id)

    def delete(self, request_id: str) -> None:
        self._items.pop(request_id, None)


class InMemoryVerificationCodeRepository:
    def __init__(self) -> None:
        self._items: dict[str, VerificationCode] = {}

    def save(self, item: VerificationCode) -> None:
        self._items[item.username] = item

    def get(self, username: str) -> VerificationCode | None:
        return self._items.get(username)

    def delete(self, username: str) -> None:
        self._items.pop(username, None)
