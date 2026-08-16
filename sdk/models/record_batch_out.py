from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.batch_item_result import BatchItemResult


T = TypeVar("T", bound="RecordBatchOut")


@_attrs_define
class RecordBatchOut:
    """
    Attributes:
        created (int):
        updated (int):
        skipped (int):
        failed (int):
        results (list[BatchItemResult]):
    """

    created: int
    updated: int
    skipped: int
    failed: int
    results: list[BatchItemResult]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created

        updated = self.updated

        skipped = self.skipped

        failed = self.failed

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "updated": updated,
                "skipped": skipped,
                "failed": failed,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.batch_item_result import BatchItemResult

        d = dict(src_dict)
        created = d.pop("created")

        updated = d.pop("updated")

        skipped = d.pop("skipped")

        failed = d.pop("failed")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = BatchItemResult.from_dict(results_item_data)

            results.append(results_item)

        record_batch_out = cls(
            created=created,
            updated=updated,
            skipped=skipped,
            failed=failed,
            results=results,
        )

        record_batch_out.additional_properties = d
        return record_batch_out

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
