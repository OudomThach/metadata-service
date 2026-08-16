from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetIn")


@_attrs_define
class DatasetIn:
    """
    Attributes:
        name (str):
        id (None | str | Unset):
        record_id (None | str | Unset):
        description (None | str | Unset):
        organization_id (int | None | Unset):
        category_id (int | None | Unset):
        collection_id (int | None | Unset):
        coverage_start (datetime.date | None | Unset):
        coverage_end (datetime.date | None | Unset):
        frequency (None | str | Unset):
        url (None | str | Unset):
        file_name (None | str | Unset):
        file_size (int | None | Unset):
        file_type (None | str | Unset):
        file_base64 (None | str | Unset):
    """

    name: str
    id: None | str | Unset = UNSET
    record_id: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    organization_id: int | None | Unset = UNSET
    category_id: int | None | Unset = UNSET
    collection_id: int | None | Unset = UNSET
    coverage_start: datetime.date | None | Unset = UNSET
    coverage_end: datetime.date | None | Unset = UNSET
    frequency: None | str | Unset = UNSET
    url: None | str | Unset = UNSET
    file_name: None | str | Unset = UNSET
    file_size: int | None | Unset = UNSET
    file_type: None | str | Unset = UNSET
    file_base64: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        record_id: None | str | Unset
        if isinstance(self.record_id, Unset):
            record_id = UNSET
        else:
            record_id = self.record_id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        organization_id: int | None | Unset
        if isinstance(self.organization_id, Unset):
            organization_id = UNSET
        else:
            organization_id = self.organization_id

        category_id: int | None | Unset
        if isinstance(self.category_id, Unset):
            category_id = UNSET
        else:
            category_id = self.category_id

        collection_id: int | None | Unset
        if isinstance(self.collection_id, Unset):
            collection_id = UNSET
        else:
            collection_id = self.collection_id

        coverage_start: None | str | Unset
        if isinstance(self.coverage_start, Unset):
            coverage_start = UNSET
        elif isinstance(self.coverage_start, datetime.date):
            coverage_start = self.coverage_start.isoformat()
        else:
            coverage_start = self.coverage_start

        coverage_end: None | str | Unset
        if isinstance(self.coverage_end, Unset):
            coverage_end = UNSET
        elif isinstance(self.coverage_end, datetime.date):
            coverage_end = self.coverage_end.isoformat()
        else:
            coverage_end = self.coverage_end

        frequency: None | str | Unset
        if isinstance(self.frequency, Unset):
            frequency = UNSET
        else:
            frequency = self.frequency

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        file_name: None | str | Unset
        if isinstance(self.file_name, Unset):
            file_name = UNSET
        else:
            file_name = self.file_name

        file_size: int | None | Unset
        if isinstance(self.file_size, Unset):
            file_size = UNSET
        else:
            file_size = self.file_size

        file_type: None | str | Unset
        if isinstance(self.file_type, Unset):
            file_type = UNSET
        else:
            file_type = self.file_type

        file_base64: None | str | Unset
        if isinstance(self.file_base64, Unset):
            file_base64 = UNSET
        else:
            file_base64 = self.file_base64

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if record_id is not UNSET:
            field_dict["record_id"] = record_id
        if description is not UNSET:
            field_dict["description"] = description
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if category_id is not UNSET:
            field_dict["category_id"] = category_id
        if collection_id is not UNSET:
            field_dict["collection_id"] = collection_id
        if coverage_start is not UNSET:
            field_dict["coverage_start"] = coverage_start
        if coverage_end is not UNSET:
            field_dict["coverage_end"] = coverage_end
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if url is not UNSET:
            field_dict["url"] = url
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
        if file_size is not UNSET:
            field_dict["file_size"] = file_size
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if file_base64 is not UNSET:
            field_dict["file_base64"] = file_base64

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_record_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        record_id = _parse_record_id(d.pop("record_id", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_organization_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        organization_id = _parse_organization_id(d.pop("organization_id", UNSET))

        def _parse_category_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        category_id = _parse_category_id(d.pop("category_id", UNSET))

        def _parse_collection_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        collection_id = _parse_collection_id(d.pop("collection_id", UNSET))

        def _parse_coverage_start(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                coverage_start_type_0 = isoparse(data).date()

                return coverage_start_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        coverage_start = _parse_coverage_start(d.pop("coverage_start", UNSET))

        def _parse_coverage_end(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                coverage_end_type_0 = isoparse(data).date()

                return coverage_end_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        coverage_end = _parse_coverage_end(d.pop("coverage_end", UNSET))

        def _parse_frequency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        frequency = _parse_frequency(d.pop("frequency", UNSET))

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_file_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

        def _parse_file_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        file_size = _parse_file_size(d.pop("file_size", UNSET))

        def _parse_file_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_type = _parse_file_type(d.pop("file_type", UNSET))

        def _parse_file_base64(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_base64 = _parse_file_base64(d.pop("file_base64", UNSET))

        dataset_in = cls(
            name=name,
            id=id,
            record_id=record_id,
            description=description,
            organization_id=organization_id,
            category_id=category_id,
            collection_id=collection_id,
            coverage_start=coverage_start,
            coverage_end=coverage_end,
            frequency=frequency,
            url=url,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            file_base64=file_base64,
        )

        dataset_in.additional_properties = d
        return dataset_in

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
