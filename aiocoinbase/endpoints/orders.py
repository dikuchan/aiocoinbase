from datetime import datetime
from decimal import Decimal
from typing import Sequence

import attrs

from .endpoint import Endpoint
from ..utils import Method
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
        return await self.request(
            endpoint=f"/orders/{order_id}",
            method=Method.GET,
            cls=Order,
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
    ) -> list[Order]:
        body = self.buildup(
            limit=limit,
            status=status,
            product_id=product_id,
            profile_id=profile_id,
            sortedBy=str(sorted_by),
            sorting=str(sorting),
            start_date=start_date.isoformat() if start_date is not None else None,
            end_date=end_date.isoformat() if end_date is not None else None,
        )

        return await self.request(
            endpoint="/orders",
            method=Method.GET,
            cls=list[Order],
            body=body,
        )

    async def cancel(
        self,
        order_id: str,
        *,
        profile_id: str | None = None,
    ) -> str:
        body = self.buildup(
            profile_id=profile_id,
        )

        return await self.request(
            endpoint=f"/orders/{order_id}",
            method=Method.DELETE,
            cls=str,
            body=body,
        )

    async def cancel_all(
        self,
        *,
        profile_id: str | None = None,
        product_id: str | None = None,
    ) -> list[str]:
        body = self.buildup(
            profile_id=profile_id,
            product_id=product_id,
        )

        return await self.request(
            endpoint="/orders",
            method=Method.DELETE,
            cls=list[str],
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
        body = self.buildup(
            profile_id=profile_id,
            type=str(order_type),
            side=str(side),
            product_id=product_id,
            stp=str(stp),
            stop=str(stop),
            stop_price=str(stop_price),
            price=str(price),
            size=str(size),
            funds=str(funds),
            time_in_force=str(time_in_force),
            cancel_after=str(cancel_after),
            post_only=post_only,
            client_oid=client_oid,
        )

        return await self.request(
            endpoint="/orders",
            method=Method.POST,
            cls=Order,
            body=body,
        )
