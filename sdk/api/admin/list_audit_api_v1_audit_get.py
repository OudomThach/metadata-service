from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_event_global_out import AuditEventGlobalOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    entity_type: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    actor_name: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_api_key, Unset):
        headers["x-api-key"] = x_api_key

    if not isinstance(x_session_token, Unset):
        headers["x-session-token"] = x_session_token

    params: dict[str, Any] = {}

    json_entity_type: None | str | Unset
    if isinstance(entity_type, Unset):
        json_entity_type = UNSET
    else:
        json_entity_type = entity_type
    params["entity_type"] = json_entity_type

    json_action: None | str | Unset
    if isinstance(action, Unset):
        json_action = UNSET
    else:
        json_action = action
    params["action"] = json_action

    json_actor_name: None | str | Unset
    if isinstance(actor_name, Unset):
        json_actor_name = UNSET
    else:
        json_actor_name = actor_name
    params["actor_name"] = json_actor_name

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/audit",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[AuditEventGlobalOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AuditEventGlobalOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[AuditEventGlobalOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    entity_type: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    actor_name: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[AuditEventGlobalOut]]:
    """List Audit

    Args:
        entity_type (None | str | Unset):
        action (None | str | Unset):
        actor_name (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AuditEventGlobalOut]]
    """

    kwargs = _get_kwargs(
        entity_type=entity_type,
        action=action,
        actor_name=actor_name,
        limit=limit,
        offset=offset,
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
    entity_type: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    actor_name: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | list[AuditEventGlobalOut] | None:
    """List Audit

    Args:
        entity_type (None | str | Unset):
        action (None | str | Unset):
        actor_name (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AuditEventGlobalOut]
    """

    return sync_detailed(
        client=client,
        entity_type=entity_type,
        action=action,
        actor_name=actor_name,
        limit=limit,
        offset=offset,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    entity_type: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    actor_name: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[AuditEventGlobalOut]]:
    """List Audit

    Args:
        entity_type (None | str | Unset):
        action (None | str | Unset):
        actor_name (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AuditEventGlobalOut]]
    """

    kwargs = _get_kwargs(
        entity_type=entity_type,
        action=action,
        actor_name=actor_name,
        limit=limit,
        offset=offset,
        x_api_key=x_api_key,
        x_session_token=x_session_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    entity_type: None | str | Unset = UNSET,
    action: None | str | Unset = UNSET,
    actor_name: None | str | Unset = UNSET,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
    x_api_key: None | str | Unset = UNSET,
    x_session_token: None | str | Unset = UNSET,
) -> HTTPValidationError | list[AuditEventGlobalOut] | None:
    """List Audit

    Args:
        entity_type (None | str | Unset):
        action (None | str | Unset):
        actor_name (None | str | Unset):
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        x_api_key (None | str | Unset):
        x_session_token (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AuditEventGlobalOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            entity_type=entity_type,
            action=action,
            actor_name=actor_name,
            limit=limit,
            offset=offset,
            x_api_key=x_api_key,
            x_session_token=x_session_token,
        )
    ).parsed
