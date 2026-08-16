from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.logout_api_v1_auth_logout_post_response_logout_api_v1_auth_logout_post import (
    LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    x_session_token: None | str | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/logout",
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    HTTPValidationError
    | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
    | None
):
    if response.status_code == 200:
        response_200 = (
            LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost.from_dict(
                response.json()
            )
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
    HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
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
    x_session_token: None | str | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
) -> Response[
    HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
]:
    """Logout

    Args:
        x_session_token (None | str | Unset):
        x_api_key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost]
    """

    kwargs = _get_kwargs(
        x_session_token=x_session_token,
        x_api_key=x_api_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    x_session_token: None | str | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
) -> (
    HTTPValidationError
    | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
    | None
):
    """Logout

    Args:
        x_session_token (None | str | Unset):
        x_api_key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
    """

    return sync_detailed(
        client=client,
        x_session_token=x_session_token,
        x_api_key=x_api_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    x_session_token: None | str | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
) -> Response[
    HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
]:
    """Logout

    Args:
        x_session_token (None | str | Unset):
        x_api_key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost]
    """

    kwargs = _get_kwargs(
        x_session_token=x_session_token,
        x_api_key=x_api_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    x_session_token: None | str | Unset = UNSET,
    x_api_key: None | str | Unset = UNSET,
) -> (
    HTTPValidationError
    | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
    | None
):
    """Logout

    Args:
        x_session_token (None | str | Unset):
        x_api_key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LogoutApiV1AuthLogoutPostResponseLogoutApiV1AuthLogoutPost
    """

    return (
        await asyncio_detailed(
            client=client,
            x_session_token=x_session_token,
            x_api_key=x_api_key,
        )
    ).parsed
