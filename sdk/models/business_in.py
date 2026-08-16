from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="BusinessIn")


@_attrs_define
class BusinessIn:
    """
    Attributes:
        date (datetime.date | None | Unset):
        tags (list[str] | None | Unset):
        domain (None | str | Unset):
        is_duplicate (bool | None | Unset):
        coverage (float | None | Unset):
    """

    date: datetime.date | None | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    domain: None | str | Unset = UNSET
    is_duplicate: bool | None | Unset = UNSET
    coverage: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date: None | str | Unset
        if isinstance(self.date, Unset):
            date = UNSET
        elif isinstance(self.date, datetime.date):
            date = self.date.isoformat()
        else:
            date = self.date

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        domain: None | str | Unset
        if isinstance(self.domain, Unset):
            domain = UNSET
        else:
            domain = self.domain

        is_duplicate: bool | None | Unset
        if isinstance(self.is_duplicate, Unset):
            is_duplicate = UNSET
        else:
            is_duplicate = self.is_duplicate

        coverage: float | None | Unset
        if isinstance(self.coverage, Unset):
            coverage = UNSET
        else:
            coverage = self.coverage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if tags is not UNSET:
            field_dict["tags"] = tags
        if domain is not UNSET:
            field_dict["domain"] = domain
        if is_duplicate is not UNSET:
            field_dict["is_duplicate"] = is_duplicate
        if coverage is not UNSET:
            field_dict["coverage"] = coverage

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_type_0 = isoparse(data).date()

                return date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        date = _parse_date(d.pop("date", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_domain(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        domain = _parse_domain(d.pop("domain", UNSET))

        def _parse_is_duplicate(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_duplicate = _parse_is_duplicate(d.pop("is_duplicate", UNSET))

        def _parse_coverage(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        coverage = _parse_coverage(d.pop("coverage", UNSET))

        business_in = cls(
            date=date,
            tags=tags,
            domain=domain,
            is_duplicate=is_duplicate,
            coverage=coverage,
        )

        business_in.additional_properties = d
        return business_in

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
