from datetime import datetime
from decimal import Decimal
from typing import Sequence

import attrs

from .endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Transfer:
    id: str
    type: str
    created_at: datetime
    completed_at: datetime
    canceled_at: datetime
    processed_at: datetime
    amount: Decimal
    details: Sequence[str]
    user_nonce: Decimal


"""
Connector.
"""


class Transfers(Endpoint):
    async def get(
        self,
        transfer_id: str,
    ) -> Transfer:
        return await self.request(
            endpoint=f"/transfers/{transfer_id}",
            method=Method.GET,
            cls=Transfer,
        )

    async def get_all(self) -> list[Transfer]:
        return await self.request(
            endpoint="/transfers",
            method=Method.GET,
            cls=list[Transfer],
        )
