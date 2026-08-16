from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.audit_event_out_snapshot import AuditEventOutSnapshot


T = TypeVar("T", bound="AuditEventOut")


@_attrs_define
class AuditEventOut:
    """
    Attributes:
        id (int):
        action (str):
        actor (str):
        at (datetime.datetime):
        snapshot (AuditEventOutSnapshot):
    """

    id: int
    action: str
    actor: str
    at: datetime.datetime
    snapshot: AuditEventOutSnapshot
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        action = self.action

        actor = self.actor

        at = self.at.isoformat()

        snapshot = self.snapshot.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "action": action,
                "actor": actor,
                "at": at,
                "snapshot": snapshot,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_event_out_snapshot import AuditEventOutSnapshot

        d = dict(src_dict)
        id = d.pop("id")

        action = d.pop("action")

        actor = d.pop("actor")

        at = isoparse(d.pop("at"))

        snapshot = AuditEventOutSnapshot.from_dict(d.pop("snapshot"))

        audit_event_out = cls(
            id=id,
            action=action,
            actor=actor,
            at=at,
            snapshot=snapshot,
        )

        audit_event_out.additional_properties = d
        return audit_event_out

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
