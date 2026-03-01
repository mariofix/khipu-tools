import hmac
import logging
import os
import re
import sys
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    cast,
    overload,
)

import typing_extensions

# Used for global variables
import khipu_tools
from khipu_tools._api_mode import ApiMode

if TYPE_CHECKING:
    from khipu_tools._api_requestor import _APIRequestor
    from khipu_tools._khipu_object import KhipuObject
    from khipu_tools._khipu_response import KhipuResponse

KHIPU_LOG = os.environ.get("KHIPU_LOG")

logger: logging.Logger = logging.getLogger("khipu")


deprecated = typing_extensions.deprecated


def _console_log_level():
    if khipu_tools.log in ["debug", "info"]:
        return khipu_tools.log
    elif KHIPU_LOG in ["debug", "info"]:
        return KHIPU_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into
        # ascii. Since the code is sent through 2to3, we can't just
        # use unicode(val, encoding='utf8') since it will be
        # translated incorrectly.
        if not isinstance(val, str):
            val = str(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return f"{key}={val}"

    return " ".join([fmt(key, val) for key, val in sorted(props.items())])


def secure_compare(val1, val2):
    return hmac.compare_digest(val1, val2)


Resp = "KhipuResponse | dict[str, Any] | list[Resp]"


@overload
def convert_to_khipu_object(
    resp: "KhipuResponse | dict[str, Any]",
    api_key: str | None = None,
    params: Mapping[str, Any] | None = None,
    klass_: type["KhipuObject"] | None = None,
    *,
    api_mode: ApiMode = "V3",
) -> "KhipuObject": ...


@overload
def convert_to_khipu_object(
    resp: list,
    api_key: str | None = None,
    params: Mapping[str, Any] | None = None,
    klass_: type["KhipuObject"] | None = None,
    *,
    api_mode: ApiMode = "V3",
) -> list["KhipuObject"]: ...


def convert_to_khipu_object(
    resp,
    api_key: str | None = None,
    params: Mapping[str, Any] | None = None,
    klass_: type["KhipuObject"] | None = None,
    *,
    api_mode: ApiMode = "V3",
) -> "KhipuObject | list[KhipuObject]":
    from khipu_tools._api_requestor import _APIRequestor

    return _convert_to_khipu_object(
        resp=resp,
        params=params,
        klass_=klass_,
        requestor=_APIRequestor._global_with_options(
            api_key=api_key,
        ),
        api_mode=api_mode,
    )


@overload
def _convert_to_khipu_object(
    *,
    resp: "KhipuResponse | dict[str, Any]",
    params: Mapping[str, Any] | None = None,
    klass_: type["KhipuObject"] | None = None,
    requestor: "_APIRequestor",
    api_mode: ApiMode,
) -> "KhipuObject": ...


@overload
def _convert_to_khipu_object(
    *,
    resp: list,
    params: Mapping[str, Any] | None = None,
    klass_: type["KhipuObject"] | None = None,
    requestor: "_APIRequestor",
    api_mode: ApiMode,
) -> list["KhipuObject"]: ...


def _convert_to_khipu_object(
    *,
    resp,
    params: Mapping[str, Any] | None = None,
    klass_: type["KhipuObject"] | None = None,
    requestor: "_APIRequestor",
    api_mode: ApiMode,
) -> "KhipuObject | list[KhipuObject]":
    # If we get a KhipuResponse, we'll want to return a
    # KhipuObject with the last_response field filled out with
    # the raw API response information
    khipu_response = None

    # Imports here at runtime to avoid circular dependencies
    from khipu_tools._khipu_object import KhipuObject
    from khipu_tools._khipu_response import KhipuResponse

    if isinstance(resp, KhipuResponse):
        khipu_response = resp
        resp = cast(Resp, khipu_response.data)

    if isinstance(resp, list):
        return [
            _convert_to_khipu_object(
                resp=cast("KhipuResponse | dict[str, Any]", i),
                requestor=requestor,
                api_mode=api_mode,
                klass_=klass_,
            )
            for i in resp
        ]
    elif isinstance(resp, dict) and not isinstance(resp, KhipuObject):
        resp = resp.copy()

        klass = KhipuObject

        obj = klass._construct_from(
            values=resp,
            last_response=khipu_response,
            requestor=requestor,
            api_mode=api_mode,
        )

        # We only need to update _retrieve_params when special params were
        # actually passed. Otherwise, leave it as is as the list / search result
        # constructors will instantiate their own params.
        if (
            params is not None
            and hasattr(obj, "object")
            and ((getattr(obj, "object") == "list") or (getattr(obj, "object") == "search_result"))
        ):
            obj._retrieve_params = params

        return obj
    else:
        return cast("KhipuObject", resp)


T = TypeVar("T")


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_api_mode() -> "ApiMode":
    return "V3"
