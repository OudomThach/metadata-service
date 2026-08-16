import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_delete_records_api_v1_records_delete_response_bulk_delete_records_api_v1_records_delete import (
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    type_: None | str | Unset = UNSET,
    domain: None | str | Unset = UNSET,
    status: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    params: dict[str, Any] = {}

    json_type_: None | str | Unset
    if isinstance(type_, Unset):
        json_type_ = UNSET
    else:
        json_type_ = type_
    params["type"] = json_type_

    json_domain: None | str | Unset
    if isinstance(domain, Unset):
        json_domain = UNSET
    else:
        json_domain = domain
    params["domain"] = json_domain

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    else:
        json_status = status
    params["status"] = json_status

    json_tag: None | str | Unset
    if isinstance(tag, Unset):
        json_tag = UNSET
    else:
        json_tag = tag
    params["tag"] = json_tag

    json_created_before: None | str | Unset
    if isinstance(created_before, Unset):
        json_created_before = UNSET
    elif isinstance(created_before, datetime.datetime):
        json_created_before = created_before.isoformat()
    else:
        json_created_before = created_before
    params["created_before"] = json_created_before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/records",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete
    | HTTPValidationError
    | None
):
    if response.status_code == 200:
        response_200 = BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete.from_dict(
            response.json()
        )

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete
    | HTTPValidationError
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    type_: None | str | Unset = UNSET,
    domain: None | str | Unset = UNSET,
    status: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete
    | HTTPValidationError
]:
    """Bulk Delete Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        created_before (datetime.datetime | None | Unset):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        type_=type_,
        domain=domain,
        status=status,
        tag=tag,
        created_before=created_before,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    type_: None | str | Unset = UNSET,
    domain: None | str | Unset = UNSET,
    status: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> (
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete
    | HTTPValidationError
    | None
):
    """Bulk Delete Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        created_before (datetime.datetime | None | Unset):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        type_=type_,
        domain=domain,
        status=status,
        tag=tag,
        created_before=created_before,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    type_: None | str | Unset = UNSET,
    domain: None | str | Unset = UNSET,
    status: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete
    | HTTPValidationError
]:
    """Bulk Delete Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        created_before (datetime.datetime | None | Unset):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        type_=type_,
        domain=domain,
        status=status,
        tag=tag,
        created_before=created_before,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    type_: None | str | Unset = UNSET,
    domain: None | str | Unset = UNSET,
    status: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    created_before: datetime.datetime | None | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> (
    BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete
    | HTTPValidationError
    | None
):
    """Bulk Delete Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        created_before (datetime.datetime | None | Unset):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
            domain=domain,
            status=status,
            tag=tag,
            created_before=created_before,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
