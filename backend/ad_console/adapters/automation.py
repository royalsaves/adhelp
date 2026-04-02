from __future__ import annotations

import requests


class NullAutomationAdapter:
    def run_unlock(self, username: str, email: str) -> None:
        print(f"[demo] unlock automation username={username} email={email}")


class HttpAutomationAdapter:
    def __init__(self, api_url: str, token: str | None) -> None:
        self._api_url = api_url
        self._token = token

    def run_unlock(self, username: str, email: str) -> None:
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        requests.post(
            self._api_url,
            headers=headers,
            json={"username": username, "email": email},
            timeout=10,
        )
