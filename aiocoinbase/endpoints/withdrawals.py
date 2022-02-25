from datetime import datetime
from decimal import Decimal

import attrs

from ..endpoint import Endpoint
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
        profile_id: str | None = None,
    ) -> Withdrawal:
        """
        Withdraws funds from the specified profile_id to a ``www.coinbase.com`` wallet.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postwithdrawcoinbaseaccount.

        Permissions: ``transfer``.

        :param amount: Amount of currency to transfer to Coinbase account.
        :param account_id: Coinbase account ID.
        :param currency: Currency to transfer.
        :param profile_id: Coinbase profile ID.
        """
        body = self.buildup(
            profile_id=profile_id,
            amount=(amount, str),
            coinbase_account_id=account_id,
            currency=currency,
        )

        return await self.request(
            "/withdrawals/coinbase-account",
            Method.POST,
            Withdrawal,
            body=body,
        )

    async def to_crypto(
        self,
        amount: Decimal,
        currency: str,
        crypto_address: str,
        *,
        profile_id: str | None = None,
        two_factor_code: str | None = None,
        nonce: int | None = None,
        fee: Decimal | None = None,
        destination_tag: str | None = None,
    ) -> Withdrawal:
        """
        Withdraws funds from the specified ``profile_id`` to an external crypto address.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postwithdrawcrypto.

        Permissions: ``transfer``.

        :param amount: Amount of currency to transfer to the crypto address.
        :param currency: Currency to transfer.
        :param crypto_address: Address of a crypto wallet.
        :param profile_id: Coinbase profile ID.
        :param two_factor_code: Two-factor code.
        :param nonce: Nonce.
        :param fee: Fee.
        :param destination_tag: Destination tag.
        """
        body = self.buildup(
            profile_id=profile_id,
            amount=(amount, str),
            currency=currency,
            crypto_address=crypto_address,
            destination_tag=destination_tag,
            no_destination_tag=destination_tag is None,
            two_factor_code=two_factor_code,
            nonce=nonce,
            fee=(fee, str),
        )

        return await self.request(
            "/withdrawals/crypto",
            Method.GET,
            Withdrawal,
            body=body,
        )

    async def to_external(
        self,
        amount: Decimal,
        method_id: str,
        currency: str,
        *,
        profile_id: str | None = None,
    ) -> Withdrawal:
        """
        Withdraws funds from the specified ``profile_id`` to a linked external payment
        method.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postwithdrawpaymentmethod.

        Permissions: ``transfer``.

        :param amount: Amount of currency to transfer.
        :param method_id: Payment method ID.
        :param currency: Currency to transfer.
        :param profile_id: Coinbase profile ID.
        """
        body = self.buildup(
            amount=(amount, str),
            payment_method_id=method_id,
            currency=currency,
            profile_id=profile_id,
        )

        return await self.request(
            "/withdrawals/payment-method",
            Method.POST,
            Withdrawal,
            body=body,
        )

    async def get_fee(
        self,
        *,
        currency: str | None = None,
        address: str | None = None,
    ) -> Decimal:
        """
        Get the fee estimate for the crypto withdrawal to crypto address.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getwithdrawfeeestimate.

        Permissions: ``transfer``.

        :param currency: Currency to transfer.
        :param address: Crypto address to transfer to.
        """
        body = self.buildup(
            currency=currency,
            crypto_address=address,
        )

        return await self.request(
            "/withdrawals/fee-estimate",
            Method.GET,
            Decimal,
            body=body,
        )
