from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_page_out import DatasetPageOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    status: None | str | Unset = UNSET,
    category_id: int | None | Unset = UNSET,
    collection_id: int | None | Unset = UNSET,
    organization_id: int | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    public: bool | Unset = False,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    params: dict[str, Any] = {}

    params["page"] = page

    params["page_size"] = page_size

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    else:
        json_status = status
    params["status"] = json_status

    json_category_id: int | None | Unset
    if isinstance(category_id, Unset):
        json_category_id = UNSET
    else:
        json_category_id = category_id
    params["category_id"] = json_category_id

    json_collection_id: int | None | Unset
    if isinstance(collection_id, Unset):
        json_collection_id = UNSET
    else:
        json_collection_id = collection_id
    params["collection_id"] = json_collection_id

    json_organization_id: int | None | Unset
    if isinstance(organization_id, Unset):
        json_organization_id = UNSET
    else:
        json_organization_id = organization_id
    params["organization_id"] = json_organization_id

    json_q: None | str | Unset
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    params["public"] = public

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/datasets",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasetPageOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DatasetPageOut.from_dict(response.json())

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
) -> Response[DatasetPageOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    status: None | str | Unset = UNSET,
    category_id: int | None | Unset = UNSET,
    collection_id: int | None | Unset = UNSET,
    organization_id: int | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    public: bool | Unset = False,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[DatasetPageOut | HTTPValidationError]:
    """List Datasets

    Args:
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        status (None | str | Unset):
        category_id (int | None | Unset):
        collection_id (int | None | Unset):
        organization_id (int | None | Unset):
        q (None | str | Unset):
        public (bool | Unset): public=1 shows only published datasets, no auth Default: False.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetPageOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        page=page,
        page_size=page_size,
        status=status,
        category_id=category_id,
        collection_id=collection_id,
        organization_id=organization_id,
        q=q,
        public=public,
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
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    status: None | str | Unset = UNSET,
    category_id: int | None | Unset = UNSET,
    collection_id: int | None | Unset = UNSET,
    organization_id: int | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    public: bool | Unset = False,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> DatasetPageOut | HTTPValidationError | None:
    """List Datasets

    Args:
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        status (None | str | Unset):
        category_id (int | None | Unset):
        collection_id (int | None | Unset):
        organization_id (int | None | Unset):
        q (None | str | Unset):
        public (bool | Unset): public=1 shows only published datasets, no auth Default: False.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetPageOut | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        page=page,
        page_size=page_size,
        status=status,
        category_id=category_id,
        collection_id=collection_id,
        organization_id=organization_id,
        q=q,
        public=public,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    status: None | str | Unset = UNSET,
    category_id: int | None | Unset = UNSET,
    collection_id: int | None | Unset = UNSET,
    organization_id: int | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    public: bool | Unset = False,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[DatasetPageOut | HTTPValidationError]:
    """List Datasets

    Args:
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        status (None | str | Unset):
        category_id (int | None | Unset):
        collection_id (int | None | Unset):
        organization_id (int | None | Unset):
        q (None | str | Unset):
        public (bool | Unset): public=1 shows only published datasets, no auth Default: False.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetPageOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        page=page,
        page_size=page_size,
        status=status,
        category_id=category_id,
        collection_id=collection_id,
        organization_id=organization_id,
        q=q,
        public=public,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    status: None | str | Unset = UNSET,
    category_id: int | None | Unset = UNSET,
    collection_id: int | None | Unset = UNSET,
    organization_id: int | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    public: bool | Unset = False,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> DatasetPageOut | HTTPValidationError | None:
    """List Datasets

    Args:
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        status (None | str | Unset):
        category_id (int | None | Unset):
        collection_id (int | None | Unset):
        organization_id (int | None | Unset):
        q (None | str | Unset):
        public (bool | Unset): public=1 shows only published datasets, no auth Default: False.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetPageOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            page_size=page_size,
            status=status,
            category_id=category_id,
            collection_id=collection_id,
            organization_id=organization_id,
            q=q,
            public=public,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
