from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.organization_in import OrganizationIn
from ...models.organization_out import OrganizationOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: int,
    *,
    body: OrganizationIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/organizations/{org_id}".format(
            org_id=quote(str(org_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | OrganizationOut | None:
    if response.status_code == 200:
        response_200 = OrganizationOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | OrganizationOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: OrganizationIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | OrganizationOut]:
    """Update Organization

    Args:
        org_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (OrganizationIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OrganizationOut]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: OrganizationIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | OrganizationOut | None:
    """Update Organization

    Args:
        org_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (OrganizationIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OrganizationOut
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    org_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: OrganizationIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | OrganizationOut]:
    """Update Organization

    Args:
        org_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (OrganizationIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OrganizationOut]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: OrganizationIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | OrganizationOut | None:
    """Update Organization

    Args:
        org_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (OrganizationIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OrganizationOut
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
