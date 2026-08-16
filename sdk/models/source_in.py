from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse
from typing_extensions import Self

from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceIn")


@_attrs_define
class SourceIn:
    """
    Attributes:
        document_id (None | str | Unset):
        filename (None | str | Unset):
        file_type (None | str | Unset):
        thumbnail_base64 (None | str | Unset):
        page (int | None | Unset):
        extracted_at (datetime.datetime | None | Unset):
        model (None | str | Unset):
        source_system (None | str | Unset):
    """

    document_id: None | str | Unset = UNSET
    filename: None | str | Unset = UNSET
    file_type: None | str | Unset = UNSET
    thumbnail_base64: None | str | Unset = UNSET
    page: int | None | Unset = UNSET
    extracted_at: datetime.datetime | None | Unset = UNSET
    model: None | str | Unset = UNSET
    source_system: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document_id: None | str | Unset
        if isinstance(self.document_id, Unset):
            document_id = UNSET
        else:
            document_id = self.document_id

        filename: None | str | Unset
        if isinstance(self.filename, Unset):
            filename = UNSET
        else:
            filename = self.filename

        file_type: None | str | Unset
        if isinstance(self.file_type, Unset):
            file_type = UNSET
        else:
            file_type = self.file_type

        thumbnail_base64: None | str | Unset
        if isinstance(self.thumbnail_base64, Unset):
            thumbnail_base64 = UNSET
        else:
            thumbnail_base64 = self.thumbnail_base64

        page: int | None | Unset
        if isinstance(self.page, Unset):
            page = UNSET
        else:
            page = self.page

        extracted_at: None | str | Unset
        if isinstance(self.extracted_at, Unset):
            extracted_at = UNSET
        elif isinstance(self.extracted_at, datetime.datetime):
            extracted_at = self.extracted_at.isoformat()
        else:
            extracted_at = self.extracted_at

        model: None | str | Unset
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        source_system: None | str | Unset
        if isinstance(self.source_system, Unset):
            source_system = UNSET
        else:
            source_system = self.source_system

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if document_id is not UNSET:
            field_dict["document_id"] = document_id
        if filename is not UNSET:
            field_dict["filename"] = filename
        if file_type is not UNSET:
            field_dict["file_type"] = file_type
        if thumbnail_base64 is not UNSET:
            field_dict["thumbnail_base64"] = thumbnail_base64
        if page is not UNSET:
            field_dict["page"] = page
        if extracted_at is not UNSET:
            field_dict["extracted_at"] = extracted_at
        if model is not UNSET:
            field_dict["model"] = model
        if source_system is not UNSET:
            field_dict["source_system"] = source_system

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_document_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        document_id = _parse_document_id(d.pop("document_id", UNSET))

        def _parse_filename(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        filename = _parse_filename(d.pop("filename", UNSET))

        def _parse_file_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_type = _parse_file_type(d.pop("file_type", UNSET))

        def _parse_thumbnail_base64(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        thumbnail_base64 = _parse_thumbnail_base64(d.pop("thumbnail_base64", UNSET))

        def _parse_page(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        page = _parse_page(d.pop("page", UNSET))

        def _parse_extracted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                extracted_at_type_0 = isoparse(data)

                return extracted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        extracted_at = _parse_extracted_at(d.pop("extracted_at", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_source_system(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_system = _parse_source_system(d.pop("source_system", UNSET))

        source_in = cls(
            document_id=document_id,
            filename=filename,
            file_type=file_type,
            thumbnail_base64=thumbnail_base64,
            page=page,
            extracted_at=extracted_at,
            model=model,
            source_system=source_system,
        )

        source_in.additional_properties = d
        return source_in

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
