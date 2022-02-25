from decimal import Decimal

import attrs

from ..endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Conversion:
    id: str
    amount: Decimal
    from_account_id: str
    to_account_id: str
    from_currency: str
    to_currency: str


"""
Connector.
"""


class Conversions(Endpoint):
    async def create(
        self,
        from_currency: str,
        to_currency: str,
        amount: Decimal,
        *,
        profile_id: str | None = None,
        nonce: str | None = None,
    ) -> Conversion:
        """
        Converts funds from ``from_currency`` currency to ``to_currency`` currency.
        Funds are converted on the ``from_currency`` account in the ``profile_id``
        profile.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postconversion.

        Permissions: ``trade``.

        Response: A successful conversion will be assigned a conversion id.
            The corresponding ledger entries for a conversion will reference this
            conversion id.

        :param from_currency: Coinbase product name to convert from.
        :param to_currency: Coinbase product name to convert to.
        :param amount: Amount of the ``from_currency`` currency to convert.
        :param profile_id: Coinbase profile ID.
        :param nonce: Nonce.
        """
        body = self.buildup(
            to=to_currency,
            amount=(amount, str),
            profile_id=profile_id,
            nonce=nonce,
            **{"from": from_currency},
        )

        return await self.request(
            "/conversions",
            Method.POST,
            Conversion,
            body=body,
        )

    async def get(
        self,
        conversion_id: str,
        *,
        profile_id: str | None = None,
    ) -> Conversion:
        """
        Gets a currency conversion by ID.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getconversion.

        :param conversion_id: Coinbase conversion ID.
        :param profile_id: Coinbase profile ID.
        """
        body = self.buildup(
            conversion_id=conversion_id,
            profile_id=profile_id,
        )

        return await self.request(
            f"/conversions/{conversion_id}",
            Method.GET,
            Conversion,
            body=body,
        )
