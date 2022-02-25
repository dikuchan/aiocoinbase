from datetime import datetime
from decimal import Decimal

import attrs

from .endpoint import Endpoint
from ..utils import Method


"""
Types.
"""


@attrs.frozen
class Withdrawal:
    id: str | None
    amount: Decimal | None
    currency: str
    payout_at: datetime
    fee: Decimal
    subtotal: Decimal


"""
Connector.
"""


class Withdrawals(Endpoint):
    async def to_account(
        self,
        amount: Decimal,
        account_id: str,
        currency: str,
        *,
        profile_id: str,
    ) -> Withdrawal:
        body = self.buildup(
            profile_id=profile_id,
            amount=str(amount),
            coinbase_account_id=account_id,
            currency=currency,
        )

        return await self.request(
            endpoint="/withdrawals/coinbase-account",
            method=Method.POST,
            cls=Withdrawal,
            body=body,
        )

    async def to_crypto(
        self,
        amount: Decimal,
        currency: str,
        crypto_address: str,
        *,
        profile_id: str,
        two_factor_code: str,
        nonce: int,
        fee: Decimal,
        destination_tag: str | None = None,
    ) -> Withdrawal:
        body = self.buildup(
            profile_id=profile_id,
            amount=str(amount),
            currency=currency,
            crypto_address=crypto_address,
            destination_tag=destination_tag,
            no_destination_tag=destination_tag is None,
            two_factor_code=two_factor_code,
            nonce=nonce,
            fee=str(fee),
        )

        return await self.request(
            endpoint="/withdrawals/crypto",
            method=Method.GET,
            cls=Withdrawal,
            body=body,
        )

    async def to_external(
        self,
        amount: Decimal,
        method_id: str,
        currency: str,
        *,
        profile_id: str,
    ) -> Withdrawal:
        body = self.buildup(
            amount=str(amount),
            payment_method_id=method_id,
            currency=currency,
            profile_id=profile_id,
        )

        return await self.request(
            endpoint="/withdrawals/payment-method",
            method=Method.POST,
            cls=Withdrawal,
            body=body,
        )

    async def get_fee(
        self,
        *,
        currency: str,
        address: str,
    ) -> Decimal:
        body = self.buildup(
            currency=currency,
            crypto_address=address,
        )

        return await self.request(
            endpoint="/withdrawals/fee-estimate",
            method=Method.GET,
            cls=Decimal,
            body=body,
        )
