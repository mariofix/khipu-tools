from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from khipu_tools._api_mode import ApiMode
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._util import merge_dicts

if TYPE_CHECKING:
    from khipu_tools._api_requestor import _APIRequestor
    from khipu_tools._khipu_response import KhipuResponse


class ErrorObject(KhipuObject):
    code: str | None
    doc_url: str | None
    message: str | None
    param: str | None
    type: str

    def refresh_from(
        self,
        values: dict[str, Any],
        api_key: str | None = None,
        partial: bool = False,
        last_response: KhipuResponse | None = None,
        *,
        api_mode: ApiMode = "V3",
    ) -> None:
        return self._refresh_from(
            values=values,
            partial=partial,
            last_response=last_response,
            requestor=self._requestor._replace_options(
                {
                    "api_key": api_key,
                }
            ),
            api_mode=api_mode,
        )

    def _refresh_from(
        self,
        *,
        values: dict[str, Any],
        partial: bool = False,
        last_response: KhipuResponse | None = None,
        requestor: _APIRequestor,
        api_mode: ApiMode,
    ) -> None:
        values = merge_dicts(
            {
                "code": None,
                "doc_url": None,
                "message": None,
                "param": None,
                "type": None,
            },
            values,
        )
        return super()._refresh_from(
            values=values,
            partial=partial,
            last_response=last_response,
            requestor=requestor,
            api_mode=api_mode,
        )
