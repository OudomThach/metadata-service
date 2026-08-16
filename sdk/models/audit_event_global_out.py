from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_event_global_out_detail_type_0 import (
        AuditEventGlobalOutDetailType0,
    )


T = TypeVar("T", bound="AuditEventGlobalOut")


@_attrs_define
class AuditEventGlobalOut:
    """
    Attributes:
        id (int):
        actor (str):
        action (str):
        entity_type (str):
        at (datetime.datetime):
        entity_id (None | str | Unset):
        detail (AuditEventGlobalOutDetailType0 | None | Unset):
    """

    id: int
    actor: str
    action: str
    entity_type: str
    at: datetime.datetime
    entity_id: None | str | Unset = UNSET
    detail: AuditEventGlobalOutDetailType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_event_global_out_detail_type_0 import (
            AuditEventGlobalOutDetailType0,
        )

        id = self.id

        actor = self.actor

        action = self.action

        entity_type = self.entity_type

        at = self.at.isoformat()

        entity_id: None | str | Unset
        if isinstance(self.entity_id, Unset):
            entity_id = UNSET
        else:
            entity_id = self.entity_id

        detail: dict[str, Any] | None | Unset
        if isinstance(self.detail, Unset):
            detail = UNSET
        elif isinstance(self.detail, AuditEventGlobalOutDetailType0):
            detail = self.detail.to_dict()
        else:
            detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "actor": actor,
                "action": action,
                "entity_type": entity_type,
                "at": at,
            }
        )
        if entity_id is not UNSET:
            field_dict["entity_id"] = entity_id
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_event_global_out_detail_type_0 import (
            AuditEventGlobalOutDetailType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        actor = d.pop("actor")

        action = d.pop("action")

        entity_type = d.pop("entity_type")

        at = isoparse(d.pop("at"))

        def _parse_entity_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        entity_id = _parse_entity_id(d.pop("entity_id", UNSET))

        def _parse_detail(
            data: object,
        ) -> AuditEventGlobalOutDetailType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                detail_type_0 = AuditEventGlobalOutDetailType0.from_dict(data)

                return detail_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuditEventGlobalOutDetailType0 | None | Unset, data)

        detail = _parse_detail(d.pop("detail", UNSET))

        audit_event_global_out = cls(
            id=id,
            actor=actor,
            action=action,
            entity_type=entity_type,
            at=at,
            entity_id=entity_id,
            detail=detail,
        )

        audit_event_global_out.additional_properties = d
        return audit_event_global_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
