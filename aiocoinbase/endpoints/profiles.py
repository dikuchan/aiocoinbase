from datetime import datetime
from decimal import Decimal

import attrs

from ..endpoint import Endpoint
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
        """
        Get information for a single profile.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getprofile.

        Permissions: ``view``.

        :param profile_id: Coinbase profile ID.
        :param active: Whether is active.
        """
        body = self.buildup(active=active)

        return await self.request(
            f"/profiles/{profile_id}",
            Method.GET,
            Profile,
            body=body,
        )

    async def get_all(
        self,
        *,
        active: bool = True,
    ) -> list[Profile]:
        """
        Gets a list of all the current user's profiles.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getprofiles.

        Permissions: ``view``.

        :param active: Whether is active.
        """
        body = self.buildup(active=active)

        return await self.request(
            "/profiles",
            Method.GET,
            list[Profile],
            body=body,
        )

    async def create(
        self,
        name: str,
    ) -> Profile:
        """
        Create a new profile.
        Will fail if user already has 10 profiles.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postprofile.

        :param name: Profile name.
        """
        body = self.buildup(name=name)

        return await self.request(
            "/profiles",
            Method.POST,
            Profile,
            body=body,
        )

    async def transfer(
        self,
        from_profile_id: str,
        to_profile_id: str,
        currency: str,
        amount: Decimal,
    ) -> None:
        """
        Transfer an amount of currency from one profile to another.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postprofiletransfer.

        Permissions: ``transfer``.

        :param from_profile_id: Coinbase profile ID to transfer funds from.
        :param to_profile_id: Coinbase profile ID to transfer funds to.
        :param currency: Currency name.
        :param amount: Amount of currency to transfer.
        """
        body = self.buildup(
            to=to_profile_id,
            currency=currency,
            amount=(amount, str),
            **{"from": from_profile_id},
        )

        return await self.request(
            "/profiles/transfer",
            Method.POST,
            None,  # type: ignore
            body=body,
        )

    async def rename(
        self,
        profile_id: str,
        name: str,
    ) -> Profile:
        """
        Rename a profile.
        Names `default` and `margin` are reserved.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_putprofile.

        :param profile_id: Coinbase profile ID.
        :param name: New name of the profile.
        """
        if name in ("default", "margin"):
            raise ValueError("Invalid profile name")

        body = self.buildup(
            profile_id=profile_id,
            name=name,
        )

        return await self.request(
            f"/profiles/{profile_id}",
            Method.PUT,
            Profile,
            body=body,
        )

    async def delete(
        self,
        profile_id: str,
        to_profile_id: str,
    ) -> None:
        """
        Delete the profile specified by ``profile_id`` and transfers all funds to the
        profile specified by ``to_profile_id``.
        Fails if there are any open orders on the profile to be deleted.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_putprofiledeactivate.

        :param profile_id: Coinbase profile ID.
        :param to_profile_id: Coinbase profile ID to transfer funds to.
        """
        body = self.buildup(
            profile_id=profile_id,
            to=to_profile_id,
        )

        return await self.request(
            f"/profiles/{profile_id}/deactivate",
            Method.PUT,
            None,  # type: ignore
            body=body,
        )
