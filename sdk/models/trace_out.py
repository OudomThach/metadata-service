from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_event_out import AuditEventOut
    from ..models.record_out import RecordOut
    from ..models.trace_out_dataset_type_0 import TraceOutDatasetType0
    from ..models.trace_out_lineage import TraceOutLineage


T = TypeVar("T", bound="TraceOut")


@_attrs_define
class TraceOut:
    """Full lineage + immutable audit chain for one record — answers "where did
    this come from, who touched it, when, and what did it become".

        Attributes:
            record (RecordOut):
            lineage (TraceOutLineage):
            audit (list[AuditEventOut]):
            dataset (None | TraceOutDatasetType0 | Unset):
    """

    record: RecordOut
    lineage: TraceOutLineage
    audit: list[AuditEventOut]
    dataset: None | TraceOutDatasetType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.trace_out_dataset_type_0 import TraceOutDatasetType0

        record = self.record.to_dict()

        lineage = self.lineage.to_dict()

        audit = []
        for audit_item_data in self.audit:
            audit_item = audit_item_data.to_dict()
            audit.append(audit_item)

        dataset: dict[str, Any] | None | Unset
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, TraceOutDatasetType0):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "record": record,
                "lineage": lineage,
                "audit": audit,
            }
        )
        if dataset is not UNSET:
            field_dict["dataset"] = dataset

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_event_out import AuditEventOut
        from ..models.record_out import RecordOut
        from ..models.trace_out_dataset_type_0 import TraceOutDatasetType0
        from ..models.trace_out_lineage import TraceOutLineage

        d = dict(src_dict)
        record = RecordOut.from_dict(d.pop("record"))

        lineage = TraceOutLineage.from_dict(d.pop("lineage"))

        audit = []
        _audit = d.pop("audit")
        for audit_item_data in _audit:
            audit_item = AuditEventOut.from_dict(audit_item_data)

            audit.append(audit_item)

        def _parse_dataset(data: object) -> None | TraceOutDatasetType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = TraceOutDatasetType0.from_dict(data)

                return dataset_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TraceOutDatasetType0 | Unset, data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        trace_out = cls(
            record=record,
            lineage=lineage,
            audit=audit,
            dataset=dataset,
        )

        trace_out.additional_properties = d
        return trace_out

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
