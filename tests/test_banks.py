import pytest
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._banks import BankItem, Banks


class MockBankItem(BankItem):
    def __init__(self):
        self.bank_id = "1"
        self.name = "Banco de Chile"
        self.message = "Este banco tiene requisitos especiales."
        self.min_amount = 1000
        self.type = "Persona"
        self.parent = "0"
        self.logo_url = "https://logo.com/banco_chile.png"


class TestBanks:

    @pytest.fixture
    def bank_item(self):
        return MockBankItem()

    @pytest.fixture
    def mock_banks(self, bank_item):
        class MockBanks(Banks):
            OBJECT_NAME = "banks"
            banks = [bank_item]

        return MockBanks()

    def test_banks_get(self, mocker):
        mocker.patch.object(Banks, "_static_request", return_value=KhipuObject())
        result = Banks.get()
        assert isinstance(result, KhipuObject)

    def test_bank_item_attributes(self, bank_item):
        assert bank_item.bank_id == "1"
        assert bank_item.name == "Banco de Chile"
        assert bank_item.message == "Este banco tiene requisitos especiales."
        assert bank_item.min_amount == 1000
        assert bank_item.type == "Persona"
        assert bank_item.parent == "0"
        assert bank_item.logo_url == "https://logo.com/banco_chile.png"

    def test_banks_attributes(self, mock_banks):
        assert mock_banks.OBJECT_NAME == "banks"
        assert len(mock_banks.banks) == 1
        assert mock_banks.banks[0].bank_id == "1"

    def test_banks_invalid_request(self, mocker):
        mocker.patch.object(Banks, "_static_request", return_value=None)
        with pytest.raises(TypeError):
            Banks.get()
