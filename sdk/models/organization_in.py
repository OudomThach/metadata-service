from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.organization_in_contact_type_0 import OrganizationInContactType0


T = TypeVar("T", bound="OrganizationIn")


@_attrs_define
class OrganizationIn:
    """
    Attributes:
        name (str):
        org_type (str | Unset):  Default: 'other'.
        contact (None | OrganizationInContactType0 | Unset):
    """

    name: str
    org_type: str | Unset = "other"
    contact: None | OrganizationInContactType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.organization_in_contact_type_0 import OrganizationInContactType0

        name = self.name

        org_type = self.org_type

        contact: dict[str, Any] | None | Unset
        if isinstance(self.contact, Unset):
            contact = UNSET
        elif isinstance(self.contact, OrganizationInContactType0):
            contact = self.contact.to_dict()
        else:
            contact = self.contact

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if org_type is not UNSET:
            field_dict["org_type"] = org_type
        if contact is not UNSET:
            field_dict["contact"] = contact

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.organization_in_contact_type_0 import OrganizationInContactType0

        d = dict(src_dict)
        name = d.pop("name")

        org_type = d.pop("org_type", UNSET)

        def _parse_contact(data: object) -> None | OrganizationInContactType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_type_0 = OrganizationInContactType0.from_dict(data)

                return contact_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OrganizationInContactType0 | Unset, data)

        contact = _parse_contact(d.pop("contact", UNSET))

        organization_in = cls(
            name=name,
            org_type=org_type,
            contact=contact,
        )

        organization_in.additional_properties = d
        return organization_in

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
