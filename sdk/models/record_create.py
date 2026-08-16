from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.audit_in import AuditIn
    from ..models.business_in import BusinessIn
    from ..models.pipeline_in import PipelineIn
    from ..models.record_create_data import RecordCreateData
    from ..models.record_in import RecordIn
    from ..models.source_in import SourceIn


T = TypeVar("T", bound="RecordCreate")


@_attrs_define
class RecordCreate:
    """
    Attributes:
        type_ (str):
        data (RecordCreateData):
        id (None | str | Unset):
        schema_version (str | Unset):  Default: '1.0'.
        source (None | SourceIn | Unset):
        audit (AuditIn | None | Unset):
        pipeline (None | PipelineIn | Unset):
        record (None | RecordIn | Unset):
        business (BusinessIn | None | Unset):
    """

    type_: str
    data: RecordCreateData
    id: None | str | Unset = UNSET
    schema_version: str | Unset = "1.0"
    source: None | SourceIn | Unset = UNSET
    audit: AuditIn | None | Unset = UNSET
    pipeline: None | PipelineIn | Unset = UNSET
    record: None | RecordIn | Unset = UNSET
    business: BusinessIn | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_in import AuditIn
        from ..models.business_in import BusinessIn
        from ..models.pipeline_in import PipelineIn
        from ..models.record_in import RecordIn
        from ..models.source_in import SourceIn

        type_ = self.type_

        data = self.data.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        schema_version = self.schema_version

        source: dict[str, Any] | None | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        elif isinstance(self.source, SourceIn):
            source = self.source.to_dict()
        else:
            source = self.source

        audit: dict[str, Any] | None | Unset
        if isinstance(self.audit, Unset):
            audit = UNSET
        elif isinstance(self.audit, AuditIn):
            audit = self.audit.to_dict()
        else:
            audit = self.audit

        pipeline: dict[str, Any] | None | Unset
        if isinstance(self.pipeline, Unset):
            pipeline = UNSET
        elif isinstance(self.pipeline, PipelineIn):
            pipeline = self.pipeline.to_dict()
        else:
            pipeline = self.pipeline

        record: dict[str, Any] | None | Unset
        if isinstance(self.record, Unset):
            record = UNSET
        elif isinstance(self.record, RecordIn):
            record = self.record.to_dict()
        else:
            record = self.record

        business: dict[str, Any] | None | Unset
        if isinstance(self.business, Unset):
            business = UNSET
        elif isinstance(self.business, BusinessIn):
            business = self.business.to_dict()
        else:
            business = self.business

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "data": data,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if source is not UNSET:
            field_dict["source"] = source
        if audit is not UNSET:
            field_dict["audit"] = audit
        if pipeline is not UNSET:
            field_dict["pipeline"] = pipeline
        if record is not UNSET:
            field_dict["record"] = record
        if business is not UNSET:
            field_dict["business"] = business

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_in import AuditIn
        from ..models.business_in import BusinessIn
        from ..models.pipeline_in import PipelineIn
        from ..models.record_create_data import RecordCreateData
        from ..models.record_in import RecordIn
        from ..models.source_in import SourceIn

        d = dict(src_dict)
        type_ = d.pop("type")

        data = RecordCreateData.from_dict(d.pop("data"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        schema_version = d.pop("schema_version", UNSET)

        def _parse_source(data: object) -> None | SourceIn | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_type_0 = SourceIn.from_dict(data)

                return source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SourceIn | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        def _parse_audit(data: object) -> AuditIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                audit_type_0 = AuditIn.from_dict(data)

                return audit_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuditIn | None | Unset, data)

        audit = _parse_audit(d.pop("audit", UNSET))

        def _parse_pipeline(data: object) -> None | PipelineIn | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pipeline_type_0 = PipelineIn.from_dict(data)

                return pipeline_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PipelineIn | Unset, data)

        pipeline = _parse_pipeline(d.pop("pipeline", UNSET))

        def _parse_record(data: object) -> None | RecordIn | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                record_type_0 = RecordIn.from_dict(data)

                return record_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RecordIn | Unset, data)

        record = _parse_record(d.pop("record", UNSET))

        def _parse_business(data: object) -> BusinessIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                business_type_0 = BusinessIn.from_dict(data)

                return business_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BusinessIn | None | Unset, data)

        business = _parse_business(d.pop("business", UNSET))

        record_create = cls(
            type_=type_,
            data=data,
            id=id,
            schema_version=schema_version,
            source=source,
            audit=audit,
            pipeline=pipeline,
            record=record,
            business=business,
        )

        record_create.additional_properties = d
        return record_create

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
