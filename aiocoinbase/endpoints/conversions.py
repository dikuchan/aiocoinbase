from decimal import Decimal

import attrs

from .endpoint import Endpoint
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
        nonce: Decimal | None = None,
    ) -> Conversion:
        body = self.buildup(
            to=to_currency,
            amount=str(amount),
            profile_id=profile_id,
            nonce=str(nonce),
            **{"from": from_currency},
        )

        return await self.request(
            endpoint="/conversions",
            method=Method.POST,
            cls=Conversion,
            body=body,
        )

    async def get(
        self,
        conversion_id: str,
        *,
        profile_id: str | None = None,
    ) -> Conversion:
        body = self.buildup(
            conversion_id=conversion_id,
            profile_id=profile_id,
        )

        return await self.request(
            endpoint=f"/conversions/{conversion_id}",
            method=Method.GET,
            cls=Conversion,
            body=body,
        )
