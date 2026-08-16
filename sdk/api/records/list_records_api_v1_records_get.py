import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.page_out import PageOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    type_: None | str | Unset = UNSET,
    domain: None | str | Unset = UNSET,
    status: None | str | Unset = UNSET,
    tag: None | str | Unset = UNSET,
    business_from: datetime.date | None | Unset = UNSET,
    business_to: datetime.date | None | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
    edited_from: datetime.datetime | None | Unset = UNSET,
    edited_to: datetime.datetime | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    sort: str | Unset = "created_at:desc",
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

    json_business_from: None | str | Unset
    if isinstance(business_from, Unset):
        json_business_from = UNSET
    elif isinstance(business_from, datetime.date):
        json_business_from = business_from.isoformat()
    else:
        json_business_from = business_from
    params["business_from"] = json_business_from

    json_business_to: None | str | Unset
    if isinstance(business_to, Unset):
        json_business_to = UNSET
    elif isinstance(business_to, datetime.date):
        json_business_to = business_to.isoformat()
    else:
        json_business_to = business_to
    params["business_to"] = json_business_to

    json_created_from: None | str | Unset
    if isinstance(created_from, Unset):
        json_created_from = UNSET
    elif isinstance(created_from, datetime.datetime):
        json_created_from = created_from.isoformat()
    else:
        json_created_from = created_from
    params["created_from"] = json_created_from

    json_created_to: None | str | Unset
    if isinstance(created_to, Unset):
        json_created_to = UNSET
    elif isinstance(created_to, datetime.datetime):
        json_created_to = created_to.isoformat()
    else:
        json_created_to = created_to
    params["created_to"] = json_created_to

    json_edited_from: None | str | Unset
    if isinstance(edited_from, Unset):
        json_edited_from = UNSET
    elif isinstance(edited_from, datetime.datetime):
        json_edited_from = edited_from.isoformat()
    else:
        json_edited_from = edited_from
    params["edited_from"] = json_edited_from

    json_edited_to: None | str | Unset
    if isinstance(edited_to, Unset):
        json_edited_to = UNSET
    elif isinstance(edited_to, datetime.datetime):
        json_edited_to = edited_to.isoformat()
    else:
        json_edited_to = edited_to
    params["edited_to"] = json_edited_to

    json_q: None | str | Unset
    if isinstance(q, Unset):
        json_q = UNSET
    else:
        json_q = q
    params["q"] = json_q

    params["page"] = page

    params["page_size"] = page_size

    params["sort"] = sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/records",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PageOut | None:
    if response.status_code == 200:
        response_200 = PageOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | PageOut]:
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
    business_from: datetime.date | None | Unset = UNSET,
    business_to: datetime.date | None | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
    edited_from: datetime.datetime | None | Unset = UNSET,
    edited_to: datetime.datetime | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    sort: str | Unset = "created_at:desc",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PageOut]:
    """List Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        business_from (datetime.date | None | Unset):
        business_to (datetime.date | None | Unset):
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):
        edited_from (datetime.datetime | None | Unset):
        edited_to (datetime.datetime | None | Unset):
        q (None | str | Unset):
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        sort (str | Unset):  Default: 'created_at:desc'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PageOut]
    """

    kwargs = _get_kwargs(
        type_=type_,
        domain=domain,
        status=status,
        tag=tag,
        business_from=business_from,
        business_to=business_to,
        created_from=created_from,
        created_to=created_to,
        edited_from=edited_from,
        edited_to=edited_to,
        q=q,
        page=page,
        page_size=page_size,
        sort=sort,
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
    business_from: datetime.date | None | Unset = UNSET,
    business_to: datetime.date | None | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
    edited_from: datetime.datetime | None | Unset = UNSET,
    edited_to: datetime.datetime | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    sort: str | Unset = "created_at:desc",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | PageOut | None:
    """List Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        business_from (datetime.date | None | Unset):
        business_to (datetime.date | None | Unset):
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):
        edited_from (datetime.datetime | None | Unset):
        edited_to (datetime.datetime | None | Unset):
        q (None | str | Unset):
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        sort (str | Unset):  Default: 'created_at:desc'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PageOut
    """

    return sync_detailed(
        client=client,
        type_=type_,
        domain=domain,
        status=status,
        tag=tag,
        business_from=business_from,
        business_to=business_to,
        created_from=created_from,
        created_to=created_to,
        edited_from=edited_from,
        edited_to=edited_to,
        q=q,
        page=page,
        page_size=page_size,
        sort=sort,
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
    business_from: datetime.date | None | Unset = UNSET,
    business_to: datetime.date | None | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
    edited_from: datetime.datetime | None | Unset = UNSET,
    edited_to: datetime.datetime | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    sort: str | Unset = "created_at:desc",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PageOut]:
    """List Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        business_from (datetime.date | None | Unset):
        business_to (datetime.date | None | Unset):
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):
        edited_from (datetime.datetime | None | Unset):
        edited_to (datetime.datetime | None | Unset):
        q (None | str | Unset):
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        sort (str | Unset):  Default: 'created_at:desc'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PageOut]
    """

    kwargs = _get_kwargs(
        type_=type_,
        domain=domain,
        status=status,
        tag=tag,
        business_from=business_from,
        business_to=business_to,
        created_from=created_from,
        created_to=created_to,
        edited_from=edited_from,
        edited_to=edited_to,
        q=q,
        page=page,
        page_size=page_size,
        sort=sort,
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
    business_from: datetime.date | None | Unset = UNSET,
    business_to: datetime.date | None | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
    edited_from: datetime.datetime | None | Unset = UNSET,
    edited_to: datetime.datetime | None | Unset = UNSET,
    q: None | str | Unset = UNSET,
    page: int | Unset = 1,
    page_size: int | Unset = 50,
    sort: str | Unset = "created_at:desc",
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | PageOut | None:
    """List Records

    Args:
        type_ (None | str | Unset):
        domain (None | str | Unset):
        status (None | str | Unset):
        tag (None | str | Unset):
        business_from (datetime.date | None | Unset):
        business_to (datetime.date | None | Unset):
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):
        edited_from (datetime.datetime | None | Unset):
        edited_to (datetime.datetime | None | Unset):
        q (None | str | Unset):
        page (int | Unset):  Default: 1.
        page_size (int | Unset):  Default: 50.
        sort (str | Unset):  Default: 'created_at:desc'.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PageOut
    """

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
            domain=domain,
            status=status,
            tag=tag,
            business_from=business_from,
            business_to=business_to,
            created_from=created_from,
            created_to=created_to,
            edited_from=edited_from,
            edited_to=edited_to,
            q=q,
            page=page,
            page_size=page_size,
            sort=sort,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
