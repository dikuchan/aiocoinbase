import base64
import hashlib
import hmac
from abc import ABC
from typing import (
    Sequence,
    Type,
    TypeAlias,
    TypeVar,
)

import aiohttp
import humps  # noqa
import orjson

from .converter import Converter
from .exceptions import (
    CoinbaseError,
    InvalidKeyError,
    InvalidRequestError,
    NoAccessError,
    NotFoundError,
)
from .utils import (
    Method,
    now,
)

PrimitiveType: TypeAlias = bool | int | str | Sequence | None


class Endpoint(ABC):
    T = TypeVar("T")

    def __init__(
        self,
        secret: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """
        Base endpoint with all the necessary defined method.

        :param secret: Coinbase Pro API secret.
        :param session: aiohttp client session.
        """
        self.secret = secret
        self.session = session
        self.converter = Converter()

    def sign(
        self,
        endpoint: str,
        method: str,
        body: str,
        timestamp: str,
    ) -> str:
        """
        Sign a payload.

        :param endpoint: Coinbase Pro API endpoint.
        :param method: HTTP request method string.
        :param body: JSON-formatted query parameters.
        :param timestamp: Current timestamp as string.

        :return: Signed payload.
        """
        message = "".join((timestamp, method, endpoint, body)).encode()
        key = base64.b64decode(self.secret)
        hashed = hmac.new(
            key=key,
            msg=message,
            digestmod=hashlib.sha256,
        )
        signature = base64.b64encode(hashed.digest()).decode()

        return signature

    @staticmethod
    def buildup(
        **params: PrimitiveType | tuple[PrimitiveType, Type],
    ) -> str:
        """
        Build-up a request body from the provided parameters.

        :param params: Request parameters.

        :return: JSON-encoded request body.
        """
        body = {}
        for key, value in params.items():
            match value:
                case None | (None, _):
                    continue
                case (param, func):
                    body[key] = func(param)
                case param:
                    body[key] = param
        params = humps.decamelize(body)
        body = orjson.dumps(params).decode()

        return body

    @staticmethod
    async def try_raise(
        status: int,
        raw: str,
    ) -> None:
        """
        Raise an exception if the provided response is invalid.

        :param status: HTTP response status code.
        :param raw: Raw response message.
        """
        if status == 200:
            return
        message = orjson.loads(raw)["message"]
        match status:
            case 400:
                raise InvalidRequestError(message)
            case 401:
                raise InvalidKeyError(message)
            case 403:
                raise NoAccessError(message)
            case 404:
                raise NotFoundError(message)
            case 500:
                raise CoinbaseError(message)

    async def request(
        self,
        endpoint: str,
        method: Method,
        cls: Type[T],
        *,
        body: str | None = None,
    ) -> T:
        """
        Send an HTTP request to Coinbase.

        :param endpoint: Coinbase REST method endpoint.
        :param method: REST API method.
        :param cls: Python class to wrap a response object into.
        :param body: JSON-encoded body of a request.

        :return: Response object.
        """
        timestamp = now()
        signature = self.sign(
            endpoint=endpoint,
            method=str(method),
            body=body if body else "",
            timestamp=timestamp,
        )
        headers = {
            "cb-access-sign": signature,
            "cb-access-timestamp": timestamp,
        }
        params = {
            "url": endpoint,
            "headers": headers,
            "data": body,
        }
        match method:
            case Method.DELETE:
                async with self.session.delete(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self.try_raise(response.status, raw)
            case Method.GET:
                async with self.session.get(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self.try_raise(response.status, raw)
            case Method.POST:
                async with self.session.post(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self.try_raise(response.status, raw)
            case Method.PUT:
                async with self.session.put(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self.try_raise(response.status, raw)

        payload = orjson.loads(raw)
        payload = humps.decamelize(payload)
        data = self.converter.structure(payload, cls)

        return data
