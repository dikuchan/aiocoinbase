from datetime import datetime
from typing import Sequence

import attrs

from ..endpoint import Endpoint
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
        """
        Get cryptographically signed prices ready to be posted on-chain using
        Compound's Open Oracle smart contract.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getcoinbasepriceoracle.

        Permissions: ``view``.
        """
        return await self.request(
            "/oracle",
            Method.GET,
            Price,
        )
