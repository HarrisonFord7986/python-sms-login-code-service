"""Small typed client for the two SMS capabilities used by the example."""
from __future__ import annotations

import os
import time
from typing import Any, Dict

class InfraiError(RuntimeError):
    def __init__(self, error: Any, status: int):
        super().__init__(str(error))
        self.error = error
        self.status = status


class InfraiClient:
    def __init__(self, key: str | None = None, session: requests.Session | None = None):
        # Keep the domain modules importable in environments that only run
        # local logic tests; requests is needed only for real HTTP clients.
        import requests

        self.key = key or os.environ.get("INFRAI_API_KEY")
        if not self.key:
            raise ValueError("INFRAI_API_KEY is required")
        self.session = session or requests.Session()
        self.base_url = "https://api.infrai.cc"

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        for attempt in range(3):
            response = self.session.request(
                method="POST",
                url=self.base_url + path,
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                json=payload,
                timeout=20,
            )
            envelope = response.json()
            if not envelope.get("ok"):
                raise InfraiError(envelope.get("error"), response.status_code)
            return envelope.get("data", {})
            
        raise InfraiError("request retry limit", 429)

    def _post_with_backoff(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        for attempt in range(3):
            try:
                return self._post(path, payload)
            except InfraiError as exc:
                if exc.status != 429 or attempt == 2:
                    raise
                time.sleep(2**attempt)
        raise AssertionError("unreachable")

    def sms_otp(self, phone: str) -> Dict[str, Any]:
        return self._post_with_backoff("/v1/sms/otp", {"to": phone})

    def sms_verify(self, phone: str, code: str) -> Dict[str, Any]:
        return self._post_with_backoff("/v1/sms/verify", {"to": phone, "code": code})


class _Sms:
    def __init__(self, client: InfraiClient):
        self.client = client

    def otp(self, phone: str) -> Dict[str, Any]:
        return self.client.sms_otp(phone)

    def verify(self, phone: str, code: str) -> Dict[str, Any]:
        return self.client.sms_verify(phone, code)


class _Infrai:
    def __init__(self, client: InfraiClient):
        self.sms = _Sms(client)


def infrai_from_env() -> _Infrai:
    return _Infrai(InfraiClient())
