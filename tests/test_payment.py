import pytest
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._request_options import RequestOptions
from khipu_tools._payments import Payments


class MockPaymentCreateResponse(KhipuObject):
    def __init__(self):
        self.payment_id = "1234"
        self.payment_url = "https://payment.url"
        self.simplified_transfer_url = "https://simplified.url"
        self.transfer_url = "https://transfer.url"
        self.app_url = "https://app.url"
        self.ready_for_terminal = True


class MockPaymentInfo(RequestOptions):
    payment_id = "1234"


class MockPaymentRefundResponse(KhipuObject):
    def __init__(self):
        self.message = "Refund successful"


class TestPayments:

    @pytest.fixture
    def payment_params(self):
        return {
            "amount": "100.00",
            "currency": "CLP",
            "subject": "Test Payment",
            "notify_api_version": "3.0",
        }

    @pytest.fixture
    def payment_info(self):
        return {"payment_id": "1234"}

    @pytest.fixture
    def payment_create_response(self):
        return MockPaymentCreateResponse()

    @pytest.fixture
    def payment_refund_response(self):
        return MockPaymentRefundResponse()

    def test_payments_create(self, payment_params, mocker):
        mocker.patch.object(Payments, "_static_request", return_value=MockPaymentCreateResponse())
        result = Payments.create(**payment_params)
        assert isinstance(result, KhipuObject)
        assert result.payment_id == "1234"
        assert result.payment_url == "https://payment.url"

    def test_payments_get(self, payment_info, mocker):
        mocker.patch.object(Payments, "_static_request", return_value=MockPaymentCreateResponse())
        result = Payments.get(**payment_info)
        assert isinstance(result, KhipuObject)
        assert result.payment_id == "1234"

    def test_payments_delete(self, payment_info, mocker):
        mocker.patch.object(Payments, "_static_request", return_value=True)
        result = Payments.delete(**payment_info)
        assert result is True

    def test_payments_refund(self, payment_info, mocker):
        mocker.patch.object(Payments, "_static_request", return_value=MockPaymentRefundResponse())
        result = Payments.refund(**payment_info)
        assert isinstance(result, KhipuObject)
        assert result.message == "Refund successful"
