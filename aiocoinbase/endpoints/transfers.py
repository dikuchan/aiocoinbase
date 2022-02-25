from datetime import datetime
from decimal import Decimal
from typing import Sequence

import attrs

from ..endpoint import Endpoint
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
        """
        Get information on a single transfer.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_gettransfer.

        Permissions: ``view``, ``trade``.

        :param transfer_id: ID of a transfer.
        """
        return await self._request(
            f"/transfers/{transfer_id}",
            Method.GET,
            Transfer,
        )

    async def get_all(self) -> list[Transfer]:
        """
        Get a list of in-progress and completed transfers of funds in and out of the
        user's accounts.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_gettransfers.

        Permissions: ``view``, ``trade``.
        """
        return await self._request(
            "/transfers",
            Method.GET,
            list[Transfer],
        )
