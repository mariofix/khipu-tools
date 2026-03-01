import calendar
import datetime
import time
from collections.abc import Generator
from typing import Any


def _encode_datetime(dttime: datetime.datetime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt="%s[%s]"):
    d = {}
    for subkey, subvalue in data.items():
        d[fmt % (key, subkey)] = subvalue
    return d


def _json_encode_date_callback(value):
    if isinstance(value, datetime.datetime):
        return _encode_datetime(value)
    return value


def _api_encode(data) -> Generator[tuple[str, Any], None, None]:
    for key, value in data.items():
        if value is None:
            continue
        elif isinstance(value, (list, tuple)):
            for i, sv in enumerate(value):
                encoded_key = "%s[%d]" % (key, i)
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict(encoded_key, sv)
                    yield from _api_encode(subdict)
                else:
                    yield (encoded_key, sv)
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            yield from _api_encode(subdict)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, value)
