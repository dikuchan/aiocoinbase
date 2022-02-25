from decimal import Decimal
from typing import Sequence

import attrs

from ..endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Currency:
    @attrs.frozen
    class Details:
        type: str | None
        symbol: str | None
        network_confirmations: int | None
        sort_order: int | None
        crypto_address_link: str | None
        crypto_transaction_link: str | None
        push_payment_methods: Sequence[str] | None
        group_types: Sequence[str] | None
        display_name: str | None
        processing_time_seconds: float | None
        min_withdrawal_amount: Decimal | None
        max_withdrawal_amount: Decimal | None

    id: str
    name: str
    min_size: Decimal
    status: str
    max_precision: Decimal
    details: Details
    message: str | None
    convertible_to: Sequence[str] | None


"""
Connector.
"""


class Currencies(Endpoint):
    async def get(
        self,
        currency_id: str,
    ) -> Currency:
        """
        Get a single currency by its ID.

        Currency codes will conform to the ISO 4217 standard where possible.
        Currencies which have or had no representation in ISO 4217 may use a custom code.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getcurrency.

        :param currency_id: Currency ID.
        """
        return await self._request(
            f"/currencies/{currency_id}",
            Method.GET,
            Currency,
        )

    async def get_all(self) -> list[Currency]:
        """
        Get a list of all known currencies.

        Note: Not all currencies may be currently in use for trading.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getcurrencies.
        """
        return await self._request(
            "/currencies",
            Method.GET,
            list[Currency],
        )
