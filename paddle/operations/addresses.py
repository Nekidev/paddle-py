from typing import Literal

from httpx import AsyncClient

from paddle.auth import BearerAuth
from paddle.schemas import (
    AddressCreate,
    AddressUpdate,
)
from paddle.exceptions import ApiError, ValidationError
from paddle.operations import Data


OrderBy = Literal[
    "id[ASC]",
    "id[DESC]",
]


class AddressOperationsMixin:
    _token: str
    _client: AsyncClient
    _endpoint: str

    async def list_customer_addresses(
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
        """List customer's addresses."""

        url = f"https://{self._endpoint}/customers/{customer_id}/addresses"

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

    async def create_customer_address(
        self,
        customer_id: str,
        address: AddressCreate,
    ) -> Data:
        """Create a customer's address."""

        url = f"https://{self._endpoint}/customers/{customer_id}/addresses"

        try:
            response = await self._client.post(
                url,
                json=address.model_dump(
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

    async def get_customer_address(
        self,
        customer_id: str,
        address_id: str,
    ) -> Data:
        """Get a customer's address."""

        url = f"https://{self._endpoint}/customers/{customer_id}/addresses/{address_id}"

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

    async def update_customer_address(
        self,
        customer_id: str,
        address_id: str,
        address: AddressUpdate,
    ) -> Data:
        """Update a customer's address."""

        url = f"https://{self._endpoint}/customers/{customer_id}/addresses/{address_id}"

        try:
            response = await self._client.patch(
                url,
                json=address.model_dump(
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
