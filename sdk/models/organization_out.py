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
    from ..models.organization_out_contact_type_0 import OrganizationOutContactType0


T = TypeVar("T", bound="OrganizationOut")


@_attrs_define
class OrganizationOut:
    """
    Attributes:
        id (int):
        name (str):
        org_type (str):
        created_at (datetime.datetime):
        contact (None | OrganizationOutContactType0 | Unset):
    """

    id: int
    name: str
    org_type: str
    created_at: datetime.datetime
    contact: None | OrganizationOutContactType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.organization_out_contact_type_0 import OrganizationOutContactType0

        id = self.id

        name = self.name

        org_type = self.org_type

        created_at = self.created_at.isoformat()

        contact: dict[str, Any] | None | Unset
        if isinstance(self.contact, Unset):
            contact = UNSET
        elif isinstance(self.contact, OrganizationOutContactType0):
            contact = self.contact.to_dict()
        else:
            contact = self.contact

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "org_type": org_type,
                "created_at": created_at,
            }
        )
        if contact is not UNSET:
            field_dict["contact"] = contact

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.organization_out_contact_type_0 import OrganizationOutContactType0

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        org_type = d.pop("org_type")

        created_at = isoparse(d.pop("created_at"))

        def _parse_contact(data: object) -> None | OrganizationOutContactType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_type_0 = OrganizationOutContactType0.from_dict(data)

                return contact_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OrganizationOutContactType0 | Unset, data)

        contact = _parse_contact(d.pop("contact", UNSET))

        organization_out = cls(
            id=id,
            name=name,
            org_type=org_type,
            created_at=created_at,
            contact=contact,
        )

        organization_out.additional_properties = d
        return organization_out

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
