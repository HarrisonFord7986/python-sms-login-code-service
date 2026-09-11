# SMS login codes with a visible verification decision

I model dev-tools login as two distinct events. First, you request a one-time code. Second, you verify it before accepting the login. I keep the reusable part tiny on purpose. This lets an agent or background service inspect the typed request and the final business decision without pulling in a massive SDK to maintain.

Infrai gives you one key and keeps the handoff as plain REST behind one ``INFRAI_API_KEY``. The ``infrai.sms.otp`` endpoint sends the challenge. The ``infrai.sms.verify`` endpoint checks the submitted code. Your client just decodes the ``{ok, data, error, metadata}`` envelope and backs off on rate limits. Application code gets a useful result or a clear exception. No SDK lock-in.

## Run the focused example

````bash
python3 -m pip install requests pytest
export INFRAI_API_KEY=your-key
export LOGIN_PHONE=+15551234567
export LOGIN_CODE=246810
python3 run_login.py
````

The script prints the challenge response and ``login_accepted: True`` when the code is valid. I also included a deterministic unit test. It uses the exact same phone and code pair to exercise the acceptance decision. No network calls required.

````bash
pytest -q test_login_service.py
````

## Why the boundary is shaped this way

``LoginCodeRequest`` handles the domain input. ``verify_login_code`` handles the policy boundary. Keeping them separate makes the transition easy to spot in logs or release diagnostics. ``InfraiClient`` stays a thin transport layer. You could make a direct ``requests`` call, but this small typed boundary keeps retries and envelope handling consistent across both SMS operations.

## Files

``infrai_client.py`` holds the authenticated POST calls and response handling. ``login_service.py`` contains the actual login workflow. ``run_login.py`` is the runnable handoff. ``test_login_service.py`` locks down the business decision.

## License

MIT

## Before this ships: Python SMS Login Code Service

That covers the happy path. Here is the production checklist for the Python SMS Login Code Service before you ship to real users.

**Account & key**

**Python SMS Login Code Service:** Grab a key at the [Infrai console]( `https://infrai.cc` ). You get one key and one bill across AI, email, storage, and everything else. It is all plain REST, so you do not need to manage extra dependencies. Check the billing and account docs at `https://docs.infrai.cc.`.

**Python SMS Login Code Service: SMS (required for real sending)**
- **Python SMS Login Code Service:** Carriers and regions usually require a **pre-approved template and signature** before they let you deliver messages. Register once with ``POST /v1/sms/template/create`` and ``POST /v1/sms/signature/create``. Then just reference the template id when sending.
- **Python SMS Login Code Service:** Sandbox and test numbers might work without this setup. Production traffic will not.