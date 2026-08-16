from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_in import CategoryIn
from ...models.category_out import CategoryOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    category_id: int,
    *,
    body: CategoryIn,
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
        "url": "/api/v1/categories/{category_id}".format(
            category_id=quote(str(category_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CategoryOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CategoryOut.from_dict(response.json())

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
) -> Response[CategoryOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    category_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CategoryIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[CategoryOut | HTTPValidationError]:
    """Update Category

    Args:
        category_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CategoryIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_id=category_id,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    category_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CategoryIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> CategoryOut | HTTPValidationError | None:
    """Update Category

    Args:
        category_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CategoryIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryOut | HTTPValidationError
    """

    return sync_detailed(
        category_id=category_id,
        client=client,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    category_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CategoryIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[CategoryOut | HTTPValidationError]:
    """Update Category

    Args:
        category_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CategoryIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_id=category_id,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    category_id: int,
    *,
    client: AuthenticatedClient | Client,
    body: CategoryIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> CategoryOut | HTTPValidationError | None:
    """Update Category

    Args:
        category_id (int):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CategoryIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            category_id=category_id,
            client=client,
            body=body,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
