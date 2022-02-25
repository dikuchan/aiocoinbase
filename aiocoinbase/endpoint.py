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

Primitive: TypeAlias = bool | int | str | Sequence | None


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
        self._secret = secret
        self._session = session
        self._converter = Converter()

    def _sign(
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
        key = base64.b64decode(self._secret)
        hashed = hmac.new(
            key=key,
            msg=message,
            digestmod=hashlib.sha256,
        )
        signature = base64.b64encode(hashed.digest()).decode()

        return signature

    @staticmethod
    def _buildup(
        **params: Primitive | tuple[Primitive, Type],
    ) -> str:
        """
        Build-up a request body from the provided parameters.

        :param params: Request parameters.

        :return: JSON-encoded request body.
        """
        processed = {}
        for key, value in params.items():
            match value:
                case None | (None, _):
                    continue
                case (param, func):
                    processed[key] = func(param)  # type: ignore
                case param:
                    processed[key] = param
        processed = humps.decamelize(processed)
        body = orjson.dumps(processed).decode()

        return body

    @staticmethod
    async def _try_raise(
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

    async def _request(
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
        signature = self._sign(
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
                async with self._session.delete(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self._try_raise(response.status, raw)
            case Method.GET:
                async with self._session.get(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self._try_raise(response.status, raw)
            case Method.POST:
                async with self._session.post(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self._try_raise(response.status, raw)
            case Method.PUT:
                async with self._session.put(**params) as response:  # type: ignore
                    raw = await response.text()
                    await self._try_raise(response.status, raw)

        payload = orjson.loads(raw)
        payload = humps.decamelize(payload)
        data = self._converter.structure(payload, cls)

        return data
