from datetime import datetime
from decimal import Decimal
from typing import Sequence

import attrs

from ..endpoint import Endpoint
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
        """
        Get information on a single product.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproduct.

        :param product_id: Coinbase product ID.
        """
        return await self._request(
            f"/products/{product_id}",
            Method.GET,
            Product,
        )

    async def get_all(self) -> list[Product]:
        """
        Get a list of available currency pairs for trading.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproducts.
        """
        return await self._request(
            "/products",
            Method.GET,
            list[Product],
        )

    async def get_book(
        self,
        product_id: str,
        level: int = 1,
    ) -> Book:
        """
        Get a list of open orders for a product.
        The amount of detail shown can be customized with the level parameter.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductbook.

        Levels:
            1 -- The best bid, ask and auction info.
            2 -- Full order book (aggregated) and auction info.
            3 -- Full order book (non aggregated) and auction info.

        :param product_id: Coinbase product ID.
        :param level: Market data depth level.
        """
        if level not in (1, 2, 3):
            raise ValueError("Invalid `level` value")

        body = self._buildup(level=level)

        return await self._request(
            f"/products/{product_id}/book",
            Method.GET,
            Book,
            body=body,
        )

    async def get_ohlc(
        self,
        product_id: str,
        *,
        period: Period = Period.Minute,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[OHLC]:
        """
        Historic OHLCV rates for a product.
        Rates are returned in grouped buckets.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles.

        Note: Historical rate data may be incomplete.
            No data is published for intervals where there are no ticks.
            Historical rates should not be polled frequently.
            If you need real-time information, use the trade and book endpoints along
            with the websocket feed.

        :param product_id: Coinbase product ID.
        :param period: OHLCV time period.
        :param start: Time for starting range of aggregations.
        :param end: Time for ending range of aggregations.
        """
        body = self._buildup(
            period=(period, int),
            start=(start, str),
            end=(end, str),
        )

        return await self._request(
            f"/products/{product_id}/candles",
            Method.GET,
            list[OHLC],
            body=body,
        )

    async def get_window(
        self,
        product_id: str,
    ) -> Window:
        """
        Gets 30 days and 24 hours window statistics for a product.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductstats.

        :param product_id: Coinbase product ID.
        """
        return await self._request(
            f"/products/{product_id}/stats",
            Method.GET,
            Window,
        )

    async def get_ticker(
        self,
        product_id: str,
    ) -> Ticker:
        """
        Gets snapshot information about the last trade (tick), best bid and ask and 24
        hours volume.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductticker.

        :param product_id: Coinbase product ID.
        """
        return await self._request(
            f"/products/{product_id}/ticker",
            Method.GET,
            Ticker,
        )

    async def get_trades(
        self,
        product_id: str,
        *,
        limit: int | None = None,
        before: datetime | None = None,
        after: datetime | None = None,
    ) -> list[Trade]:
        """
        Get a list of the latest trades for a product.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproducttrades.

        :param product_id: Coinbase product ID.
        :param limit: Limit of trades in one response.
        :param before: Used for pagination. Sets start cursor to ``before`` date.
        :param after: Used for pagination. Sets end cursor to ``after`` date.
        """
        body = self._buildup(
            limit=limit,
            before=(before, str),
            after=(after, str),
        )

        return await self._request(
            f"/products/{product_id}/trades",
            Method.GET,
            list[Trade],
            body=body,
        )
