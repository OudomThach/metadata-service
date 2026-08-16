from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuditIn")


@_attrs_define
class AuditIn:
    """
    Attributes:
        created_at (datetime.datetime | None | Unset):
        created_by (None | str | Unset):
        edited_at (datetime.datetime | None | Unset):
        edited_by (None | str | Unset):
        edit_count (int | None | Unset):
        status (None | str | Unset):
        raw_ref (None | str | Unset):
    """

    created_at: datetime.datetime | None | Unset = UNSET
    created_by: None | str | Unset = UNSET
    edited_at: datetime.datetime | None | Unset = UNSET
    edited_by: None | str | Unset = UNSET
    edit_count: int | None | Unset = UNSET
    status: None | str | Unset = UNSET
    raw_ref: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        edited_at: None | str | Unset
        if isinstance(self.edited_at, Unset):
            edited_at = UNSET
        elif isinstance(self.edited_at, datetime.datetime):
            edited_at = self.edited_at.isoformat()
        else:
            edited_at = self.edited_at

        edited_by: None | str | Unset
        if isinstance(self.edited_by, Unset):
            edited_by = UNSET
        else:
            edited_by = self.edited_by

        edit_count: int | None | Unset
        if isinstance(self.edit_count, Unset):
            edit_count = UNSET
        else:
            edit_count = self.edit_count

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        raw_ref: None | str | Unset
        if isinstance(self.raw_ref, Unset):
            raw_ref = UNSET
        else:
            raw_ref = self.raw_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if edited_by is not UNSET:
            field_dict["edited_by"] = edited_by
        if edit_count is not UNSET:
            field_dict["edit_count"] = edit_count
        if status is not UNSET:
            field_dict["status"] = status
        if raw_ref is not UNSET:
            field_dict["raw_ref"] = raw_ref

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_edited_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                edited_at_type_0 = isoparse(data)

                return edited_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        edited_at = _parse_edited_at(d.pop("edited_at", UNSET))

        def _parse_edited_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        edited_by = _parse_edited_by(d.pop("edited_by", UNSET))

        def _parse_edit_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        edit_count = _parse_edit_count(d.pop("edit_count", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_raw_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        raw_ref = _parse_raw_ref(d.pop("raw_ref", UNSET))

        audit_in = cls(
            created_at=created_at,
            created_by=created_by,
            edited_at=edited_at,
            edited_by=edited_by,
            edit_count=edit_count,
            status=status,
            raw_ref=raw_ref,
        )

        audit_in.additional_properties = d
        return audit_in

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
