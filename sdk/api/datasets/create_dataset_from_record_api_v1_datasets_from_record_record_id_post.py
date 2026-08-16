from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_out import DatasetOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    record_id: str,
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
        "method": "post",
        "url": "/api/v1/datasets/from-record/{record_id}".format(
            record_id=quote(str(record_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasetOut | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = DatasetOut.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DatasetOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    record_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[DatasetOut | HTTPValidationError]:
    """Create Dataset From Record

     Lift a record's post-OCR dataset payload (data.dataset + embedded file
    + columns + references) into a first-class Dataset row (status draft).

    Args:
        record_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        record_id=record_id,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    record_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> DatasetOut | HTTPValidationError | None:
    """Create Dataset From Record

     Lift a record's post-OCR dataset payload (data.dataset + embedded file
    + columns + references) into a first-class Dataset row (status draft).

    Args:
        record_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetOut | HTTPValidationError
    """

    return sync_detailed(
        record_id=record_id,
        client=client,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    record_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[DatasetOut | HTTPValidationError]:
    """Create Dataset From Record

     Lift a record's post-OCR dataset payload (data.dataset + embedded file
    + columns + references) into a first-class Dataset row (status draft).

    Args:
        record_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        record_id=record_id,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    record_id: str,
    *,
    client: AuthenticatedClient | Client,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> DatasetOut | HTTPValidationError | None:
    """Create Dataset From Record

     Lift a record's post-OCR dataset payload (data.dataset + embedded file
    + columns + references) into a first-class Dataset row (status draft).

    Args:
        record_id (str):
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            record_id=record_id,
            client=client,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
