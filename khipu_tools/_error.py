from typing import cast

import khipu_tools  # noqa
from khipu_tools._error_object import ErrorObject


class KhipuError(Exception):
    _message: str | None
    http_body: str | None
    http_status: int | None
    json_body: object | None
    headers: dict[str, str] | None
    code: str | None
    request_id: str | None
    error: "ErrorObject | None"

    def __init__(
        self,
        message: str | None = None,
        http_body: bytes | str | None = None,
        http_status: int | None = None,
        json_body: object | None = None,
        headers: dict[str, str] | None = None,
        code: str | None = None,
    ):
        super().__init__(message)

        body: Optional[str] = None
        if http_body:
            # http_body can sometimes be a memoryview which must be cast
            # to a "bytes" before calling decode, so we check for the
            # decode attribute and then cast
            if hasattr(http_body, "decode"):
                try:
                    body = cast(bytes, http_body).decode("utf-8")
                except (UnicodeDecodeError, ValueError):
                    body = "<Could not decode body as utf-8. Please open an issue at https://github.com/mariofix/khipu-tools/issues>"
            elif isinstance(http_body, str):
                body = http_body

        self._message = message
        self.http_body = body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.request_id = None
        self.error = self._construct_error_object()

    def __str__(self):
        msg = self._message or "<empty message>"
        if self.request_id is not None:
            return f"Request {self.request_id}: {msg}"
        else:
            return msg

    # Returns the underlying `Exception` (base class) message, which is usually
    # the raw message returned by Khipu's API. This was previously available
    # in python2 via `error.message`. Unlike `str(error)`, it omits "Request
    # req_..." from the beginning of the string.
    @property
    def user_message(self):
        return self._message

    def __repr__(self):
        return "{}(message={!r}, http_status={!r}, request_id={!r})".format(
            self.__class__.__name__,
            self._message,
            self.http_status,
            self.request_id,
        )

    def _construct_error_object(self) -> "ErrorObject | None":
        if (
            self.json_body is None
            or not isinstance(self.json_body, dict)
            or "error" not in self.json_body
            or not isinstance(self.json_body["error"], dict)
        ):
            return None
        from khipu_tools._error_object import ErrorObject

        return ErrorObject._construct_from(
            values=self.json_body["error"],
            requestor=khipu_tools._APIRequestor._global_instance(),
            api_mode="V3",
        )


class APIError(KhipuError):
    pass


class APIConnectionError(KhipuError):
    should_retry: bool

    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        super().__init__(message, http_body, http_status, json_body, headers, code)
        self.should_retry = should_retry


class KhipuErrorWithParamCode(KhipuError):
    def __repr__(self):
        return "%s(message=%r, param=%r, code=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.param,  # pyright: ignore
            self.code,
            self.http_status,
            self.request_id,
        )


class IdempotencyError(KhipuError):
    pass


class InvalidRequestError(KhipuErrorWithParamCode):
    def __init__(
        self,
        message,
        param,
        code=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        super().__init__(message, http_body, http_status, json_body, headers, code)
        self.param = param


class AuthenticationError(KhipuError):
    pass


class PermissionError(KhipuError):
    pass


class RateLimitError(KhipuError):
    pass


class SignatureVerificationError(KhipuError):
    def __init__(self, message, sig_header, http_body=None):
        super().__init__(message, http_body)
        self.sig_header = sig_header


# classDefinitions: The beginning of the section generated from our OpenAPI spec
class TemporarySessionExpiredError(KhipuError):
    pass


# classDefinitions: The end of the section generated from our OpenAPI spec
