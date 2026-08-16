from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.record_batch_in import RecordBatchIn
from ...models.record_batch_out import RecordBatchOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: RecordBatchIn,
    on_duplicate: str | Unset = "error",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    params: dict[str, Any] = {}

    params["on_duplicate"] = on_duplicate

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/records/batch",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecordBatchOut | None:
    if response.status_code == 200:
        response_200 = RecordBatchOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | RecordBatchOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RecordBatchIn,
    on_duplicate: str | Unset = "error",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecordBatchOut]:
    """Create Records Batch

     Ingest up to 500 records in one call. Each item is processed in its own
    transaction slice — a failure in one item never rolls back the others.

    Args:
        on_duplicate (str | Unset):  Default: 'error'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (RecordBatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecordBatchOut]
    """

    kwargs = _get_kwargs(
        body=body,
        on_duplicate=on_duplicate,
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
    body: RecordBatchIn,
    on_duplicate: str | Unset = "error",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | RecordBatchOut | None:
    """Create Records Batch

     Ingest up to 500 records in one call. Each item is processed in its own
    transaction slice — a failure in one item never rolls back the others.

    Args:
        on_duplicate (str | Unset):  Default: 'error'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (RecordBatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecordBatchOut
    """

    return sync_detailed(
        client=client,
        body=body,
        on_duplicate=on_duplicate,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RecordBatchIn,
    on_duplicate: str | Unset = "error",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecordBatchOut]:
    """Create Records Batch

     Ingest up to 500 records in one call. Each item is processed in its own
    transaction slice — a failure in one item never rolls back the others.

    Args:
        on_duplicate (str | Unset):  Default: 'error'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (RecordBatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecordBatchOut]
    """

    kwargs = _get_kwargs(
        body=body,
        on_duplicate=on_duplicate,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RecordBatchIn,
    on_duplicate: str | Unset = "error",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | RecordBatchOut | None:
    """Create Records Batch

     Ingest up to 500 records in one call. Each item is processed in its own
    transaction slice — a failure in one item never rolls back the others.

    Args:
        on_duplicate (str | Unset):  Default: 'error'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (RecordBatchIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecordBatchOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            on_duplicate=on_duplicate,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
