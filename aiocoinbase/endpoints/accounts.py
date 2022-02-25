from datetime import datetime
from decimal import Decimal
from typing import TypeAlias

import attrs

from ..endpoint import Endpoint
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
        """
        Get information for a single account.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccount.

        Permissions: ``view``, ``trade``.

        :param account_id: Coinbase account ID.
        """
        return await self.request(
            f"/accounts/{account_id}",
            Method.GET,
            Account,
        )

    async def get_all(self) -> list[Account]:
        """
        Get a list of trading accounts from the profile of the API key.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccounts.

        Permissions: ``view``, ``trade``.

        Limits: 25 requests per second, up to 50 requests per second in bursts.
        """
        return await self.request(
            "/accounts",
            Method.GET,
            list[Account],
        )

    async def get_holds(
        self,
        account_id: str,
        *,
        before: datetime | None = None,
        after: datetime | None = None,
        limit: int = 100,
    ) -> list[Hold]:
        """
        List the holds of an account that belong to the same profile as the API key.

        Holds are placed on an account for any active orders or pending withdraw
        requests.
        As an order is filled, the hold amount is updated.
        If an order is canceled, any remaining hold is removed.
        For withdrawals, the hold is removed after it is completed.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccountholds.

        :param account_id: Coinbase account ID.
        :param before: Used for pagination. Sets start cursor to ``before`` date.
        :param after: Used for pagination. Sets end cursor to ``after`` date.
        :param limit: Limit on number of results to return.
        """
        body = self.buildup(
            before=(before, str),
            after=(after, str),
            limit=limit,
        )

        return await self.request(
            f"/accounts/{account_id}/holds",
            Method.GET,
            list[Hold],
            body=body,
        )

    async def get_ledger(
        self,
        account_id: str,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        before: datetime | None = None,
        after: datetime | None = None,
        limit: int = 100,
        profile_id: str | None = None,
    ) -> Ledger:
        """
        Lists ledger activity for an account.
        This includes anything that would affect the accounts balance: transfers,
        trades, fees, etc.

        List account activity of the API key's profile.
        Account activity either increases or decreases your account balance.
        Items are paginated and sorted latest first.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccountledger.

        Permissions: ``view``, ``trade``.

        :param account_id: Coinbase account ID.
        :param start_date: Filter results by minimum posted date.
        :param end_date: Filter results by maximum posted date.
        :param before: Used for pagination. Sets start cursor to ``before`` date.
        :param after: Used for pagination. Sets end cursor to ``after`` date.
        :param limit: Limit on number of results to return.
        :param profile_id: Coinbase profile ID.
        """
        body = self.buildup(
            start_date=(start_date, str),
            end_date=(end_date, str),
            before=(before, str),
            after=(after, str),
            limit=limit,
            profile_id=profile_id,
        )

        return await self.request(
            f"/accounts/{account_id}/ledger",
            Method.GET,
            Ledger,
            body=body,
        )

    async def get_transfers(
        self,
        account_id: str,
        *,
        before: datetime | None = None,
        after: datetime | None = None,
        limit: int = 100,
        type: str | None = None,
    ) -> list[Transfer]:
        """
        Lists past withdrawals and deposits for an account.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getaccounttransfers.

        :param account_id: Coinbase account ID.
        :param before: Used for pagination. Sets start cursor to ``before`` date.
        :param after: Used for pagination. Sets end cursor to ``after`` date.
        :param limit: Limit on number of results to return.
        :param type: Type of transfers to filter by.
        """
        body = self.buildup(
            before=(before, str),
            after=(after, str),
            limit=limit,
            type=type,
        )

        return await self.request(
            f"/accounts/{account_id}/transfers",
            Method.GET,
            list[Transfer],
            body=body,
        )
