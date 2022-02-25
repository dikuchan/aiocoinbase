from datetime import datetime
from decimal import Decimal
from typing import Sequence

import attrs

from .endpoint import Endpoint
from ..types import Period
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Product:
    id: str
    base_currency: str
    quote_currency: str
    base_min_size: Decimal
    base_max_size: Decimal
    quote_increment: Decimal
    base_increment: Decimal
    display_name: str
    min_market_funds: Decimal
    max_market_funds: Decimal
    margin_enabled: bool
    post_only: bool
    limit_only: bool
    cancel_only: bool
    status: str
    status_message: str
    trading_disabled: bool | None
    fx_stablecoin: bool | None
    max_slippage_percentage: Decimal | None
    auction_mode: bool


@attrs.frozen
class Book:
    @attrs.frozen
    class Auction:
        open_price: Decimal
        open_size: Decimal
        best_bid_price: Decimal
        best_bid_size: Decimal
        best_ask_price: Decimal
        best_ask_size: Decimal
        auction_state: str
        can_open: str | None
        time: datetime | None

    bids: Sequence[str]
    asks: Sequence[str]
    sequence: Decimal
    auction_mode: bool | None
    auction: Auction | None


@attrs.frozen
class OHLC:
    time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal


@attrs.frozen
class Ticker:
    trade_id: int
    ask: Decimal
    bid: Decimal
    volume: Decimal
    price: Decimal
    size: Decimal
    time: datetime


@attrs.frozen
class Trade:
    trade_id: int
    side: str
    size: Decimal
    price: Decimal
    time: datetime


@attrs.frozen
class Window:
    open: Decimal
    high: Decimal
    low: Decimal
    last: Decimal
    volume: Decimal
    volume_30day: Decimal


"""
Connector.
"""


class Products(Endpoint):
    async def get(
        self,
        product_id: str,
    ) -> Product:
        return await self.request(
            endpoint=f"/products/{product_id}",
            method=Method.GET,
            cls=Product,
        )

    async def get_all(self) -> list[Product]:
        return await self.request(
            endpoint="/products",
            method=Method.GET,
            cls=list[Product],
        )

    async def get_book(
        self,
        product_id: str,
        level: int = 1,
    ) -> Book:
        if level not in (1, 2, 3):
            raise ValueError("Invalid `level` value")

        body = self.buildup(level=level)

        return await self.request(
            endpoint=f"/products/{product_id}/book",
            method=Method.GET,
            cls=Book,
            body=body,
        )

    async def get_ohlc(
        self,
        product_id: str,
        *,
        period: Period = Period.Minute,
        start: datetime,
        end: datetime,
    ) -> list[OHLC]:
        body = self.buildup(
            period=int(period),
            start=str(start),
            end=str(end),
        )

        return await self.request(
            endpoint=f"/products/{product_id}/candles",
            method=Method.GET,
            cls=list[OHLC],
            body=body,
        )

    async def get_window(
        self,
        product_id: str,
    ) -> Window:
        return await self.request(
            endpoint=f"/products/{product_id}/stats",
            method=Method.GET,
            cls=Window,
        )

    async def get_ticker(
        self,
        product_id: str,
    ) -> Ticker:
        return await self.request(
            endpoint=f"/products/{product_id}/ticker",
            method=Method.GET,
            cls=Ticker,
        )

    async def get_trades(
        self,
        product_id: str,
    ) -> list[Trade]:
        return await self.request(
            endpoint=f"/products/{product_id}/trades",
            method=Method.GET,
            cls=list[Trade],
        )
