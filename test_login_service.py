from login_service import LoginCodeRequest, verify_login_code


class FakeSms:
    def verify(self, phone, code):
        return {"verified": phone == "+15551234567" and code == "246810"}


class FakeInfrai:
    sms = FakeSms()


def test_login_decision_accepts_matching_code():
    assert verify_login_code(FakeInfrai(), LoginCodeRequest("+15551234567", "246810")) is True
