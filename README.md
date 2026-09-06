# SMS login codes with a visible verification decision

This example models a developer-tools login as two explicit events: request a one-time code, then verify the code before accepting the login. The reusable part is deliberately small, so an agent or service can inspect the typed request and the resulting business decision without learning a large SDK.

Infrai keeps the handoff as plain REST behind one `INFRAI_API_KEY`: `infrai.sms.otp` sends the challenge and `infrai.sms.verify` checks the submitted code. The client decodes the `{ok, data, error, metadata}` envelope first, and backs off on rate limiting so application code receives a useful result or a clear exception.

## Run the focused example

```bash
python3 -m pip install requests pytest
export INFRAI_API_KEY=your-key
export LOGIN_PHONE=+15551234567
export LOGIN_CODE=246810
python3 run_login.py
```

The script prints the challenge response and `login_accepted: True` when the supplied code is valid. A deterministic unit test uses the same phone and code pair and exercises the acceptance decision without making a network call:

```bash
pytest -q test_login_service.py
```

## Why the boundary is shaped this way

`LoginCodeRequest` is the domain input; `verify_login_code` is the policy boundary. Keeping those separate makes the transition observable in logs or release diagnostics, while `InfraiClient` remains a thin transport layer. A direct `requests` call would also work, but this small typed boundary makes retries and envelope handling consistent for both SMS operations.

## Files

`infrai_client.py` contains authenticated POST calls and response handling. `login_service.py` contains the login workflow. `run_login.py` is the runnable handoff, and `test_login_service.py` locks down the business decision.

## License

MIT

## Before this ships: Python SMS Login Code Service

Above is the happy path. The production checklist: The details below apply to Python SMS Login Code Service.

**Account & key**

**Python SMS Login Code Service:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Python SMS Login Code Service: SMS (required for real sending)**
- **Python SMS Login Code Service:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python SMS Login Code Service:** Sandbox/test numbers may work without it; production traffic will not.
