from datetime import datetime
from typing import Sequence

import attrs

from ..endpoint import Endpoint
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
        """
        Get a specific report by ``report_id``.

        Note: Once a report request has been accepted for processing, the status is
            available by polling the report resource endpoint.
            The final report will be uploaded and available at ``file_url`` once the
            ``status`` indicates ``ready``.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getreport.

        Permissions: ``view``, ``trade``.

        :param report_id: ID of a report.
        """
        return await self._request(
            f"/reports/{report_id}",
            Method.GET,
            Report,
        )

    async def get_all(
        self,
        *,
        portfolio_id: str | None = None,
        after: datetime | None = None,
        limit: int = 100,
        report_type: ReportType = ReportType.Fills,
        ignore_expired: bool = True,
    ) -> list[Report]:
        """
        Get a list of past fills and account reports.

        Note: Once a report request has been accepted for processing, the status is
            available by polling the report resource endpoint.
            The final report will be uploaded and available at ``file_url`` once the
            ``status`` indicates ``ready``.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getreports.

        Permission: ``view``, ``trade``.

        :param portfolio_id: Filter results by a specific ``profile_id``.
        :param after: Filter results after a specific date.
        :param limit: Limit results to a specific number.
        :param report_type: Filter results by type of report (fills or account).
        :param ignore_expired: Whether to ignore expired results.
        """
        body = self._buildup(
            portfolio_id=portfolio_id,
            after=(after, str),
            limit=limit,
            type=(report_type, str),
            ignore_expired=ignore_expired,
        )

        return await self._request(
            "/reports",
            Method.GET,
            list[Report],
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
        """
        Generate a report.
        Reports are either for past account history or past fills on either all accounts
        or one product's account.

        Docs: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_postreports.

        Permissions: ``view``, ``trade``.

        Expired reports: Reports are only available for download for a few days after
            being created.
            Once a report expires, the report is no longer available for download and is
            deleted.

        :param report_type: Type of report.
        :param start_date: Start date for items to be included in report.
        :param end_date: End datetime for items to be included in report.
        :param year: Required for transaction history type reports.
        :param report_format: PDF or CSV.
        :param product_id: Product, required for fills-type reports.
        :param account_id: Account, required for account-type reports.
        :param email: Email to send generated report to.
        :param profile_id: Which portfolio to generate the report for.
        """
        body = self._buildup(
            start_date=(start_date, str),
            end_date=(end_date, str),
            type=(report_type, str),
            year=year,
            format=(report_format, str),
            product_id=product_id,
            account_id=account_id,
            email=email,
            profile_id=profile_id,
        )

        return await self._request(
            "/reports",
            Method.POST,
            CreateResponse,
            body=body,
        )
