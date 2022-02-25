from decimal import Decimal

import attrs

from ..endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Fee:
    taker_fee_rate: Decimal
    maker_fee_rate: Decimal
    usd_volume: Decimal | None


"""
Connector.
"""


class Fees(Endpoint):
    async def get(self) -> list[Fee]:
        """
        Get fees rates and 30 days trailing volume.

        This request will return your current maker & taker fee rates, as well as your
        30-day trailing volume.
        Quoted rates are subject to change.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getfees.

        Permissions: ``view``.
        """
        return await self.request(
            "/fees",
            Method.GET,
            list[Fee],
        )
