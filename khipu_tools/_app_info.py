from typing import TypedDict


class AppInfo(TypedDict):
    name: str
    url: str | None
    version: str | None
