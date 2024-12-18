from collections.abc import Iterable

from .items import ErrorItem


class BaseError(Exception):
    def __init__(self, status, message):
        self._status = status
        self._message = message

    @classmethod
    def from_data(cls, data):
        return cls(data.get("status"), data.get("message"))

    @property
    def status(self):
        """
        Código del error
        """
        return self._status

    @property
    def message(self):
        """
        Mensaje del error
        """
        return self._message

    def __str__(self):
        return f"{self._status} {self._message}"


class AuthorizationError(BaseError):
    pass


class ServiceError(BaseError):
    pass


class ValidationError(BaseError):
    def __init__(self, status, message, errors):
        super().__init__(status, message)
        self._errors = errors if errors and errors is Iterable else []

    @classmethod
    def from_data(cls, data):
        errors = [ErrorItem.from_data(i) for i in data.get("errors")]
        return cls(data.get("status"), data.get("message"), errors)

    @property
    def errors(self):
        """
        Arreglo de ErrorItems
        """
        return self._errors
