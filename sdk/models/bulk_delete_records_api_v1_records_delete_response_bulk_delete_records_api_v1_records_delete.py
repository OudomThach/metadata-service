from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar(
    "T",
    bound="BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete",
)


@_attrs_define
class BulkDeleteRecordsApiV1RecordsDeleteResponseBulkDeleteRecordsApiV1RecordsDelete:
    """ """

    additional_properties: dict[str, int] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        bulk_delete_records_api_v1_records_delete_response_bulk_delete_records_api_v1_records_delete = cls()

        bulk_delete_records_api_v1_records_delete_response_bulk_delete_records_api_v1_records_delete.additional_properties = d
        return bulk_delete_records_api_v1_records_delete_response_bulk_delete_records_api_v1_records_delete

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> int:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
