from datetime import datetime
from decimal import Decimal

import attrs

from .endpoint import Endpoint
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Profile:
    id: str
    user_id: str
    name: str
    active: bool
    is_default: bool
    has_margin: bool | None
    created_at: datetime


"""
Connector.
"""


class Profiles(Endpoint):
    async def get(
        self,
        profile_id: str,
        *,
        active: bool = True,
    ) -> Profile:
        body = self.buildup(active=active)

        return await self.request(
            endpoint=f"/profiles/{profile_id}",
            method=Method.GET,
            cls=Profile,
            body=body,
        )

    async def get_all(
        self,
        *,
        active: bool = True,
    ) -> list[Profile]:
        body = self.buildup(active=active)

        return await self.request(
            endpoint="/profiles",
            method=Method.GET,
            cls=list[Profile],
            body=body,
        )

    async def create(
        self,
        name: str,
    ) -> Profile:
        body = self.buildup(name=name)

        return await self.request(
            endpoint="/profiles",
            method=Method.POST,
            cls=Profile,
            body=body,
        )

    async def transfer(
        self,
        from_profile_id: str,
        to_profile_id: str,
        currency: str,
        amount: Decimal,
    ) -> None:
        body = self.buildup(
            to=to_profile_id,
            currency=currency,
            amount=str(amount),
            **{"from": from_profile_id},
        )

        return await self.request(
            endpoint="/profiles/transfer",
            method=Method.POST,
            cls=None,  # type: ignore
            body=body,
        )

    async def rename(
        self,
        profile_id: str,
        name: str,
    ) -> Profile:
        if name in ("default", "margin"):
            raise ValueError("Invalid profile name")

        body = self.buildup(
            profile_id=profile_id,
            name=name,
        )

        return await self.request(
            endpoint=f"/profiles/{profile_id}",
            method=Method.PUT,
            cls=Profile,
            body=body,
        )

    async def delete(
        self,
        profile_id: str,
        to_profile_id: str,
    ) -> None:
        body = self.buildup(
            profile_id=profile_id,
            to=to_profile_id,
        )

        return await self.request(
            endpoint=f"/profiles/{profile_id}/deactivate",
            method=Method.PUT,
            cls=None,  # type: ignore
            body=body,
        )
