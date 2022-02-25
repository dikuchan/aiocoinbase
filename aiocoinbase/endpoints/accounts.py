from datetime import datetime
from decimal import Decimal
from typing import (
    TypeAlias,
)

import attrs

from .endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Account:
    id: str
    currency: str
    balance: Decimal
    available: Decimal
    hold: Decimal
    profile_id: str
    trading_enabled: bool


@attrs.frozen
class Hold:
    id: str
    created_at: datetime
    updated_at: datetime
    type: str
    ref: str


@attrs.frozen
class Activity:
    id: str
    amount: Decimal
    created_at: datetime
    balance: Decimal
    type: str
    details: str


Ledger: TypeAlias = list[Activity]


@attrs.frozen
class Transfer:
    id: str
    type: str
    created_at: datetime
    completed_at: datetime
    canceled_at: datetime
    processed_at: datetime
    amount: Decimal
    details: str
    user_nonce: Decimal


"""
Connector.
"""


class Accounts(Endpoint):
    async def get(
        self,
        account_id: str,
    ) -> Account:
        return await self.request(
            endpoint=f"/accounts/{account_id}",
            method=Method.GET,
            cls=Account,
        )

    async def get_all(self) -> list[Account]:
        return await self.request(
            endpoint="/accounts",
            method=Method.GET,
            cls=list[Account],
        )

    async def get_holds(
        self,
        account_id: str,
    ) -> list[Hold]:
        return await self.request(
            endpoint=f"/accounts/{account_id}/holds",
            method=Method.GET,
            cls=list[Hold],
        )

    async def get_ledger(
        self,
        account_id: str,
    ) -> Ledger:
        return await self.request(
            endpoint=f"/accounts/{account_id}/ledger",
            method=Method.GET,
            cls=Ledger,
        )

    async def get_transfers(
        self,
        account_id: str,
    ) -> list[Transfer]:
        return await self.request(
            endpoint=f"/accounts/{account_id}/transfers",
            method=Method.GET,
            cls=list[Transfer],
        )
