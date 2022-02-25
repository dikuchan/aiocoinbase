from datetime import datetime
from decimal import Decimal

import attrs

from ..endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Deposit:
    id: str | None = None
    amount: Decimal | None = None
    currency: str | None = None
    payout_at: datetime | None = None
    fee: Decimal | None = None
    subtotal: Decimal | None = None


"""
Connector.
"""


class Deposits(Endpoint):
    async def create(
        self,
        amount: Decimal,
        account_id: str,
        currency: str,
        *,
        profile_id: str | None = None,
    ) -> Deposit:
        """
        Deposits funds from a `www.coinbase.com` wallet to the specified ``profile_id``.

        Note: You can move funds between your Coinbase accounts and your Coinbase
            Exchange trading accounts within your daily limits.
            Moving funds between Coinbase and Coinbase Exchange is instant and free.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postdepositcoinbaseaccount.

        Permissions: ``transfer``.

        :param amount: Amount of funds to deposit.
        :param account_id: Coinbase account ID.
        :param currency: Coinbase product name to deposit.
        :param profile_id: Coinbase profile ID.
        """
        body = self._buildup(
            amount=(amount, str),
            coinbase_account_id=account_id,
            currency=currency,
            profile_id=profile_id,
        )

        return await self._request(
            "/deposits/coinbase-account",
            Method.POST,
            Deposit,
            body=body,
        )

    async def create_external(
        self,
        amount: Decimal,
        method_id: str,
        currency: str,
        *,
        profile_id: str | None = None,
    ) -> Deposit:
        """
        Deposits funds from a linked external payment method to the specified
        ``profile_id``.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postdepositpaymentmethod.

        Permissions: ``transfer``.

        :param amount: Amount of funds to deposit.
        :param method_id: External method ID.
        :param currency: Coinbase product name to deposit.
        :param profile_id: Coinbase profile ID.
        """
        body = self._buildup(
            amount=(amount, str),
            payment_method_id=method_id,
            currency=currency,
            profile_id=profile_id,
        )

        return await self._request(
            "/deposits/payment-method",
            Method.POST,
            Deposit,
            body=body,
        )
