from datetime import datetime
from decimal import Decimal
from typing import Sequence

import attrs

from ..endpoint import Endpoint
from ..types import (
    CancelAfter,
    OrderType,
    SelfTradePrevention,
    Side,
    SortedBy,
    Sorting,
    StopOrderType,
    TimeInForce,
)
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Order:
    id: str
    product_id: str
    side: str
    type: str
    time_in_force: str
    expire_time: datetime
    post_only: bool
    created_at: datetime
    fill_fees: Decimal
    filled_size: Decimal
    status: str
    settled: bool
    price: Decimal | None
    size: Decimal | None
    profile_id: str | None
    funds: Decimal | None
    specified_funds: Decimal | None
    done_at: datetime | None
    done_reason: str | None
    reject_reason: str | None
    executed_value: str | None
    stop: str | None
    stop_price: Decimal | None
    funding_amount: Decimal | None
    client_iod: str | None


"""
Connector.
"""


class Orders(Endpoint):
    async def get(
        self,
        order_id: str,
    ) -> Order:
        """
        Get a single order by ``order_id``.

        If the order is canceled the response may have status code 404 if the order had
        no matches.

        Note: Open orders may change state between the request and the response
            depending on market conditions.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getorder.

        Permissions: ``view``, ``trade``.

        :param order_id: either the exchange assigned id or the client assigned
            ``client_oid``.
            When using ``client_oid`` it must be preceded by the ``client: namespace``.
        """
        return await self._request(
            f"/orders/{order_id}",
            Method.GET,
            Order,
        )

    async def get_all(
        self,
        limit: int = 100,
        status: Sequence[str] = None,
        *,
        profile_id: str | None = None,
        product_id: str | None = None,
        sorted_by: SortedBy | None = None,
        sorting: Sorting | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        before: datetime | None = None,
        after: datetime | None = None,
    ) -> list[Order]:
        """
        List your current open orders.

        Only open or un-settled orders are returned by default.
        As soon as an order is no longer open and settled, it will no longer appear in
        the default request.
        Open orders may change state between the request and the response depending on
        market conditions.

        Note: Note that orders with a `pending` status have a reduced set of fields in
            the response.
            `Pending` limit orders will not have ``stp``, ``time_in_force``,
            ``expire_time``, and ``post_only``.
            `Pending` market orders will have the same fields as a `pending` limit order
            minus ``price`` and ``size``, and no market specific fields (``funds``,
            ``specified_funds``).
            `Pending` stop orders will have the same fields as a `pending` limit order
            and no stop specific fields (``stop``, ``stop_price``).

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getorders.

        Permissions: ``view``, ``trade``.

        Order status: Orders which are no longer resting on the order book, will be
            marked with the done status.
            There is a small window between an order being done and settled.
            An order is settled when all the fills have settled and the remaining holds
            (if any) have been removed.

        Polling: For high-volume trading it is strongly recommended that you maintain
            your own list of open orders and use one of the streaming market data feeds
            to keep it updated.
            You should poll the open orders' endpoint once when you start trading to
            obtain the current state of any open orders.

        :param limit: Limit on number of results to return.
        :param status: List with order statuses to filter by.
        :param profile_id: Filter results by a specific Coinbase ``profile_id``.
        :param product_id: Filter results by a specific Coinbase ``product_id``.
        :param sorted_by: Sort criteria for results.
        :param sorting: Ascending or descending order.
        :param start_date: Filter results by minimum posted date.
        :param end_date: Filter results by maximum posted date.
        :param before: Used for pagination. Sets start cursor to ``before`` date.
        :param after: Used for pagination. Sets end cursor to ``after`` date.
        """
        body = self._buildup(
            limit=limit,
            status=status,
            product_id=product_id,
            profile_id=profile_id,
            sortedBy=(sorted_by, str),
            sorting=(sorting, str),
            start_date=(start_date, str),
            end_date=(end_date, str),
            before=(before, str),
            after=(after, str),
        )

        return await self._request(
            "/orders",
            Method.GET,
            list[Order],
            body=body,
        )

    async def cancel(
        self,
        order_id: str,
        *,
        profile_id: str | None = None,
    ) -> str:
        """
        Cancel a single open order by ``id``.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_deleteorder.

        Permissions: ``trade``.

        Response: Successfully cancelled order response will include the order ID if
            requested cancellation is by exchange assigned ``id``, or the client
            assigned ``client_oid`` if cancelled by client order ID.

        Cancel reject: If the order could not be canceled (already filled or previously
            canceled, etc.), then an error response will indicate the reason in the
            message field.

        :param order_id: ``id`` of the order to cancel.
        :param profile_id: Cancels orders on a specific Coinbase profile.

        :return: ``id`` of the order that was cancelled.
        """
        body = self._buildup(profile_id=profile_id)

        return await self._request(
            f"/orders/{order_id}",
            Method.DELETE,
            str,
            body=body,
        )

    async def cancel_all(
        self,
        *,
        profile_id: str | None = None,
        product_id: str | None = None,
    ) -> list[str]:
        """
        With the best effort, cancel all open orders.
        This may require you to make the request multiple times until all the open
        orders are deleted.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_deleteorders.

        Permissions: ``trade``.

        :param profile_id: Cancels orders on a specific profile.
        :param product_id: Cancels orders on a specific product only.

        :return: A list of the ``id``s of open orders that were successfully cancelled.
        """
        body = self._buildup(
            profile_id=profile_id,
            product_id=product_id,
        )

        return await self._request(
            "/orders",
            Method.DELETE,
            list[str],
            body=body,
        )

    async def create(
        self,
        side: Side,
        product_id: str,
        *,
        profile_id: str = "default",
        order_type: OrderType = OrderType.Limit,
        stp: SelfTradePrevention = SelfTradePrevention.DecreaseCancel,
        stop: StopOrderType = StopOrderType.Loss,
        stop_price: Decimal,
        price: Decimal,
        size: Decimal,
        funds: Decimal,
        time_in_force: TimeInForce = TimeInForce.GoodTillCanceled,
        cancel_after: CancelAfter = CancelAfter.Min,
        post_only: bool = False,
        client_oid: str | None = None,
    ) -> Order:
        """
        Create an order.

        You can place two types of orders: limit and market.
        Orders can only be placed if your account has sufficient funds.
        Once an order is placed, your account funds will be put on hold for the duration
        of the order.
        How much and which funds are put on hold depends on the order type and
        parameters specified.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postorders.

        Permissions: ``trade``.

        :param side: Trade side (buy or sell).
        :param product_id: Book on which to place an order.
        :param profile_id: Create order on a specific ``profile_id``.
            If None, default to `default` profile.
        :param order_type: Limit, market or stop order type.
        :param stp: Self-trade prevention type.
        :param stop: Stop order type (loss or entry).
        :param stop_price: Price threshold at which a stop order will be placed on the
            book.
        :param price: Price per unit of cryptocurrency, required for limit and stop
            orders.
        :param size: Amount of base currency to buy or sell, required for limit and stop
            orders and market sells.
        :param funds: Amount of quote currency to buy, required for market buys.
        :param time_in_force: Lifetime of an order policy.
        :param cancel_after: Min, hour or day.
        :param post_only: If true, order will only execute as a maker order.
        :param client_oid: Optional Order ID selected to identify the order.
        """
        body = self._buildup(
            profile_id=profile_id,
            type=(order_type, str),
            side=(side, str),
            product_id=product_id,
            stp=(stp, str),
            stop=(stop, str),
            stop_price=(stop_price, str),
            price=(price, str),
            size=(size, str),
            funds=(funds, str),
            time_in_force=(time_in_force, str),
            cancel_after=(cancel_after, str),
            post_only=post_only,
            client_oid=client_oid,
        )

        return await self._request(
            "/orders",
            Method.POST,
            Order,
            body=body,
        )
