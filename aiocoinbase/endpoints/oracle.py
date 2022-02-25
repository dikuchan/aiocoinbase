from datetime import datetime
from typing import Sequence

import attrs

from .endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Price:
    timestamp: datetime
    messages: Sequence[str]
    signatures: Sequence[str]
    prices: str


"""
Connector.
"""


class Oracle(Endpoint):
    async def get(self) -> Price:
        return await self.request(
            endpoint=f"/oracle",
            method=Method.GET,
            cls=Price,
        )
