from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.change_password_api_v1_auth_me_password_post_response_change_password_api_v1_auth_me_password_post import (
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.password_change_in import PasswordChangeIn
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PasswordChangeIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/me/password",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost
    | HTTPValidationError
    | None
):
    if response.status_code == 200:
        response_200 = ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost.from_dict(
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
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost
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
    body: PasswordChangeIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost
    | HTTPValidationError
]:
    """Change Password

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (PasswordChangeIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
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
    body: PasswordChangeIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> (
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost
    | HTTPValidationError
    | None
):
    """Change Password

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (PasswordChangeIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PasswordChangeIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost
    | HTTPValidationError
]:
    """Change Password

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (PasswordChangeIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PasswordChangeIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> (
    ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost
    | HTTPValidationError
    | None
):
    """Change Password

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (PasswordChangeIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
