from __future__ import annotations

import requests


class NullNotificationAdapter:
    def send(self, message: str) -> None:
        print(f"[demo] notification: {message}")


class SlackNotificationAdapter:
    def __init__(self, webhook_url: str) -> None:
        self._webhook_url = webhook_url

    def send(self, message: str) -> None:
        requests.post(self._webhook_url, json={"text": message}, timeout=5)
