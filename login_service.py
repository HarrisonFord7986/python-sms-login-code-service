from dataclasses import dataclass
from typing import Any, Dict

from infrai_client import _Infrai


@dataclass(frozen=True)
class LoginCodeRequest:
    phone: str
    code: str


def send_login_code(infrai: _Infrai, phone: str) -> Dict[str, Any]:
    """Start the login challenge; the returned data identifies the SMS operation."""
    return infrai.sms.otp(phone)


def verify_login_code(infrai: _Infrai, request: LoginCodeRequest) -> bool:
    """Return the business decision, keeping transport details out of callers."""
    result = infrai.sms.verify(request.phone, request.code)
    return bool(result.get("verified", result.get("valid", False)))
