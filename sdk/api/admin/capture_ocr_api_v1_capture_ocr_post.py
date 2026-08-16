from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.capture_ocr_in import CaptureOcrIn
from ...models.http_validation_error import HTTPValidationError
from ...models.record_out import RecordOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CaptureOcrIn,
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
        "url": "/api/v1/capture-ocr",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecordOut | None:
    if response.status_code == 201:
        response_201 = RecordOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | RecordOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CaptureOcrIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecordOut]:
    """Capture Ocr

     Save an OCR result with all artifacts generated server-side.

    Requires X-API-Key or a session token (the adapters call this with the
    service's own API key when an OCR request carries save=true). Generates
    markdown + csv (pipe tables -> CSV with BOM) and stores the raw result as
    data.json — the Option-B path for direct API callers.

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CaptureOcrIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecordOut]
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
    body: CaptureOcrIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | RecordOut | None:
    """Capture Ocr

     Save an OCR result with all artifacts generated server-side.

    Requires X-API-Key or a session token (the adapters call this with the
    service's own API key when an OCR request carries save=true). Generates
    markdown + csv (pipe tables -> CSV with BOM) and stores the raw result as
    data.json — the Option-B path for direct API callers.

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CaptureOcrIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecordOut
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
    body: CaptureOcrIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecordOut]:
    """Capture Ocr

     Save an OCR result with all artifacts generated server-side.

    Requires X-API-Key or a session token (the adapters call this with the
    service's own API key when an OCR request carries save=true). Generates
    markdown + csv (pipe tables -> CSV with BOM) and stores the raw result as
    data.json — the Option-B path for direct API callers.

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CaptureOcrIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecordOut]
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
    body: CaptureOcrIn,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | RecordOut | None:
    """Capture Ocr

     Save an OCR result with all artifacts generated server-side.

    Requires X-API-Key or a session token (the adapters call this with the
    service's own API key when an OCR request carries save=true). Generates
    markdown + csv (pipe tables -> CSV with BOM) and stores the raw result as
    data.json — the Option-B path for direct API callers.

    Args:
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):
        body (CaptureOcrIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecordOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
