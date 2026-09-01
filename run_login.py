import os

from infrai_client import infrai_from_env
from login_service import LoginCodeRequest, send_login_code, verify_login_code


def main() -> None:
    phone = os.environ.get("LOGIN_PHONE")
    code = os.environ.get("LOGIN_CODE")
    if not phone or not code:
        raise SystemExit("Set LOGIN_PHONE and LOGIN_CODE")
    infrai = infrai_from_env()
    challenge = send_login_code(infrai, phone)
    accepted = verify_login_code(infrai, LoginCodeRequest(phone, code))
    print({"challenge": challenge, "login_accepted": accepted})


if __name__ == "__main__":
    main()
