from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    *,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/datasets/{dataset_id}/file".format(
            dataset_id=quote(str(dataset_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Download Dataset File

     Raw download of a published dataset's embedded file (public). Draft or
    archived datasets require admin/editor.

    Args:
        dataset_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Download Dataset File

     Raw download of a published dataset's embedded file (public). Draft or
    archived datasets require admin/editor.

    Args:
        dataset_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        dataset_id=dataset_id,
        client=client,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Download Dataset File

     Raw download of a published dataset's embedded file (public). Draft or
    archived datasets require admin/editor.

    Args:
        dataset_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Download Dataset File

     Raw download of a published dataset's embedded file (public). Draft or
    archived datasets require admin/editor.

    Args:
        dataset_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            client=client,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
