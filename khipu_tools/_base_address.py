from typing import Literal, TypedDict
from typing_extensions import NotRequired

BaseAddress = Literal["api"]


class BaseAddresses(TypedDict):
    api: NotRequired[str | None]
