from datetime import datetime
from decimal import Decimal

import attrs

from .endpoint import Endpoint
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
        body = self.buildup(
            amount=str(amount),
            coinbase_account_id=account_id,
            currency=currency,
            profile_id=profile_id,
        )

        response = await self.request(
            endpoint="/deposits/coinbase-account",
            method=Method.POST,
            cls=Deposit,
            body=body,
        )

        return response

    async def create_external(
        self,
        amount: Decimal,
        method_id: str,
        currency: str,
        *,
        profile_id: str | None = None,
    ) -> Deposit:
        body = self.buildup(
            amount=str(amount),
            payment_method_id=method_id,
            currency=currency,
            profile_id=profile_id,
        )

        response = await self.request(
            endpoint="/deposits/payment-method",
            method=Method.POST,
            cls=Deposit,
            body=body,
        )

        return response
