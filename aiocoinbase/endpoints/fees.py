from decimal import Decimal

import attrs

from .endpoint import Endpoint
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
        return await self.request(
            endpoint="/fees",
            method=Method.GET,
            cls=list[Fee],
        )
