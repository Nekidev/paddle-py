from typing import Literal

from httpx import AsyncClient

from paddle.auth import BearerAuth
from paddle.schemas import (
    BusinessCreate,
    BusinessUpdate,
)
from paddle.exceptions import ApiError, ValidationError
from paddle.operations import Data


OrderBy = Literal[
    "id[ASC]",
    "id[DESC]",
]


class BusinessOperationsMixin:
    _token: str
    _client: AsyncClient
    _endpoint: str

    async def list_customer_businesses(
        self,
        customer_id: str,
        *,
        after: str = ...,
        id: list[str] = ...,
        order_by: OrderBy = ...,
        per_page: int = 200,
        search: str = ...,
        status: list[Literal["active", "archived"]] = ...,
    ) -> Data:
        """List customer's businesses."""

        url = f"https://{self._endpoint}/customers/{customer_id}/businesses"

        query = {}

        if after is not ...:
            query["after"] = after

        if id is not ...:
            query["id"] = ",".join(id)

        if order_by is not ...:
            query["order_by"] = order_by

        if per_page is not ...:
            query["per_page"] = per_page

        if search is not ...:
            query["search"] = search

        if status is not ...:
            query["status"] = ",".join(status)

        try:
            response = await self._client.get(
                url,
                params=query,
                auth=BearerAuth(self._token),
            )

        except Exception as e:
            raise ApiError from e

        try:
            response.raise_for_status()

        except Exception as e:
            raise ApiError(response.text) from e

        try:
            return response.json()

        except Exception as e:
            raise ValidationError from e

    async def create_customer_business(
        self,
        customer_id: str,
        business: BusinessCreate,
    ) -> Data:
        """Create a customer's business."""

        url = f"https://{self._endpoint}/customers/{customer_id}/businesses"

        try:
            response = await self._client.post(
                url,
                json=business.model_dump(
                    mode="json", exclude_unset=True, exclude_defaults=True
                ),
                auth=BearerAuth(self._token),
            )

        except Exception as e:
            raise ApiError from e

        try:
            response.raise_for_status()

        except Exception as e:
            raise ApiError(response.text) from e

        try:
            return response.json()

        except Exception as e:
            raise ValidationError from e

    async def get_customer_business(
        self,
        customer_id: str,
        business_id: str,
    ) -> Data:
        """Get a customer's business."""

        url = (
            f"https://{self._endpoint}/customers/{customer_id}/businesses/{business_id}"
        )

        try:
            response = await self._client.get(
                url,
                auth=BearerAuth(self._token),
            )

        except Exception as e:
            raise ApiError from e

        try:
            response.raise_for_status()

        except Exception as e:
            raise ApiError(response.text) from e

        try:
            return response.json()

        except Exception as e:
            raise ValidationError from e

    async def update_customer_business(
        self,
        customer_id: str,
        business_id: str,
        business: BusinessUpdate,
    ) -> Data:
        """Update a customer's business."""

        url = (
            f"https://{self._endpoint}/customers/{customer_id}/businesses/{business_id}"
        )

        try:
            response = await self._client.patch(
                url,
                json=business.model_dump(
                    mode="json", exclude_unset=True, exclude_defaults=True
                ),
                auth=BearerAuth(self._token),
            )

        except Exception as e:
            raise ApiError from e

        try:
            response.raise_for_status()

        except Exception as e:
            raise ApiError(response.text) from e

        try:
            return response.json()

        except Exception as e:
            raise ValidationError from e
