import pytest
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._predict import Predict


class TestPredict:

    @pytest.fixture
    def predict_params(self):
        return {"payer_email": "test@example.com", "bank_id": "123", "amount": "100.00", "currency": "CLP"}

    @pytest.fixture
    def mock_predict_result(self):
        class MockPredict(Predict):
            OBJECT_NAME = "predict"
            result = "ok"
            max_amount = 100000
            cool_down_date = "2025-01-21"
            new_destinatary_max_amount = "50000"

        return MockPredict()

    def test_predict_get(self, predict_params, mocker):
        mocker.patch.object(Predict, "_static_request", return_value=KhipuObject())
        result = Predict.get(**predict_params)
        assert isinstance(result, KhipuObject)

    def test_predict_attributes(self, mock_predict_result):
        assert mock_predict_result.result == "ok"
        assert mock_predict_result.max_amount == 100000
        assert mock_predict_result.cool_down_date == "2025-01-21"
        assert mock_predict_result.new_destinatary_max_amount == "50000"

    def test_predict_invalid_request(self, mocker):
        mocker.patch.object(Predict, "_static_request", return_value=None)
        with pytest.raises(TypeError):
            Predict.get(payer_email="test@example.com")
