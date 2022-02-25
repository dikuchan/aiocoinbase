from datetime import datetime
from typing import Sequence

import attrs

from .endpoint import Endpoint
from ..types import (
    ReportFormat,
    ReportType,
)
from ..utils import Method

"""
Types.
"""


@attrs.frozen
class Report:
    @attrs.frozen
    class Parameters:
        @attrs.frozen
        class User:
            id: str
            created_at: datetime
            active_at: datetime
            name: str
            email: str
            roles: Sequence[str]
            is_banned: bool
            user_type: str
            fulfills_new_requirements: str
            flags: Sequence[str] | None
            details: Sequence[str] | None
            preferences: Sequence[str]
            has_default: bool
            state_code: str | None
            cb_data_from_cache: bool | None
            two_factor_method: str | None
            legal_name: str | None
            terms_accepted: datetime | None
            has_clawback_payment_pending: bool | None
            has_restricted_assets: bool | None

        start_date: datetime
        end_date: datetime
        format: str
        product_id: str
        account_id: str
        profile_id: str
        email: str
        user: User
        new_york_state: bool

    id: str
    type: str
    created_at: datetime
    completed_at: datetime
    expires_at: datetime
    status: str
    user_id: str
    file_url: str
    params: Parameters
    file_count: str | None


@attrs.frozen
class CreateResponse:
    id: str
    type: ReportType
    status: str


"""
Connector.
"""


class Reports(Endpoint):
    async def get(
        self,
        report_id: str,
    ) -> Report:
        return await self.request(
            endpoint=f"/reports/{report_id}",
            method=Method.GET,
            cls=Report,
        )

    async def get_all(
        self,
        *,
        portfolio_id: str,
        after: datetime,
        limit: int = 100,
        report_type: ReportType = ReportType.Fills,
        ignore_expired: bool = True,
    ) -> list[Report]:
        body = self.buildup(
            portfolio_id=portfolio_id,
            after=str(after),
            limit=limit,
            type=str(report_type),
            ignore_expired=ignore_expired,
        )

        return await self.request(
            endpoint="/reports",
            method=Method.GET,
            cls=list[Report],
            body=body,
        )

    async def create(
        self,
        report_type: ReportType,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        year: str | None,
        report_format: ReportFormat = ReportFormat.PDF,
        product_id: str = "ALL",
        account_id: str = "ALL",
        email: str | None = None,
        profile_id: str | None = None,
    ) -> CreateResponse:
        body = self.buildup(
            start_date=str(start_date) if start_date else None,
            end_date=str(end_date) if end_date else None,
            type=str(report_type),
            year=year,
            format=str(report_format),
            product_id=product_id,
            account_id=account_id,
            email=email,
            profile_id=profile_id,
        )

        return await self.request(
            endpoint="/reports",
            method=Method.POST,
            cls=CreateResponse,
            body=body,
        )
