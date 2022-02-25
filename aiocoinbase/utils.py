from datetime import datetime, tzinfo
from enum import Enum


class Method(Enum):
    DELETE = "DELETE"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"

    def __str__(self) -> str:
        return self.value


def now(tz: tzinfo | None = None) -> str:
    """
    Get current timestamp in seconds.
    """
    return str(datetime.now(tz=tz).timestamp())
