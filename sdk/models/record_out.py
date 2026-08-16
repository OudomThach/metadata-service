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
    from ..models.audit_in import AuditIn
    from ..models.business_in import BusinessIn
    from ..models.pipeline_in import PipelineIn
    from ..models.record_in import RecordIn
    from ..models.record_out_data import RecordOutData
    from ..models.record_out_envelope import RecordOutEnvelope
    from ..models.source_in import SourceIn


T = TypeVar("T", bound="RecordOut")


@_attrs_define
class RecordOut:
    """
    Attributes:
        id (str):
        schema_version (str):
        type_ (str):
        domain (None | str):
        status (str):
        business_date (datetime.date | None):
        tags (list[str] | None):
        data (RecordOutData):
        envelope (RecordOutEnvelope):
        created_at (datetime.datetime):
        created_by (str):
        edited_at (datetime.datetime | None):
        edited_by (None | str):
        edit_count (int):
        source (None | SourceIn | Unset):
        audit (AuditIn | None | Unset):
        pipeline (None | PipelineIn | Unset):
        record (None | RecordIn | Unset):
        business (BusinessIn | None | Unset):
        source_model (None | str | Unset):
        source_system (None | str | Unset):
    """

    id: str
    schema_version: str
    type_: str
    domain: None | str
    status: str
    business_date: datetime.date | None
    tags: list[str] | None
    data: RecordOutData
    envelope: RecordOutEnvelope
    created_at: datetime.datetime
    created_by: str
    edited_at: datetime.datetime | None
    edited_by: None | str
    edit_count: int
    source: None | SourceIn | Unset = UNSET
    audit: AuditIn | None | Unset = UNSET
    pipeline: None | PipelineIn | Unset = UNSET
    record: None | RecordIn | Unset = UNSET
    business: BusinessIn | None | Unset = UNSET
    source_model: None | str | Unset = UNSET
    source_system: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.audit_in import AuditIn
        from ..models.business_in import BusinessIn
        from ..models.pipeline_in import PipelineIn
        from ..models.record_in import RecordIn
        from ..models.source_in import SourceIn

        id = self.id

        schema_version = self.schema_version

        type_ = self.type_

        domain: None | str
        domain = self.domain

        status = self.status

        business_date: None | str
        if isinstance(self.business_date, datetime.date):
            business_date = self.business_date.isoformat()
        else:
            business_date = self.business_date

        tags: list[str] | None
        if isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        data = self.data.to_dict()

        envelope = self.envelope.to_dict()

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        edited_at: None | str
        if isinstance(self.edited_at, datetime.datetime):
            edited_at = self.edited_at.isoformat()
        else:
            edited_at = self.edited_at

        edited_by: None | str
        edited_by = self.edited_by

        edit_count = self.edit_count

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

        source_model: None | str | Unset
        if isinstance(self.source_model, Unset):
            source_model = UNSET
        else:
            source_model = self.source_model

        source_system: None | str | Unset
        if isinstance(self.source_system, Unset):
            source_system = UNSET
        else:
            source_system = self.source_system

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "schema_version": schema_version,
                "type": type_,
                "domain": domain,
                "status": status,
                "business_date": business_date,
                "tags": tags,
                "data": data,
                "envelope": envelope,
                "created_at": created_at,
                "created_by": created_by,
                "edited_at": edited_at,
                "edited_by": edited_by,
                "edit_count": edit_count,
            }
        )
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
        if source_model is not UNSET:
            field_dict["source_model"] = source_model
        if source_system is not UNSET:
            field_dict["source_system"] = source_system

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.audit_in import AuditIn
        from ..models.business_in import BusinessIn
        from ..models.pipeline_in import PipelineIn
        from ..models.record_in import RecordIn
        from ..models.record_out_data import RecordOutData
        from ..models.record_out_envelope import RecordOutEnvelope
        from ..models.source_in import SourceIn

        d = dict(src_dict)
        id = d.pop("id")

        schema_version = d.pop("schema_version")

        type_ = d.pop("type")

        def _parse_domain(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        domain = _parse_domain(d.pop("domain"))

        status = d.pop("status")

        def _parse_business_date(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                business_date_type_0 = isoparse(data).date()

                return business_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None, data)

        business_date = _parse_business_date(d.pop("business_date"))

        def _parse_tags(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        tags = _parse_tags(d.pop("tags"))

        data = RecordOutData.from_dict(d.pop("data"))

        envelope = RecordOutEnvelope.from_dict(d.pop("envelope"))

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        def _parse_edited_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                edited_at_type_0 = isoparse(data)

                return edited_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        edited_at = _parse_edited_at(d.pop("edited_at"))

        def _parse_edited_by(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        edited_by = _parse_edited_by(d.pop("edited_by"))

        edit_count = d.pop("edit_count")

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

        def _parse_source_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_model = _parse_source_model(d.pop("source_model", UNSET))

        def _parse_source_system(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_system = _parse_source_system(d.pop("source_system", UNSET))

        record_out = cls(
            id=id,
            schema_version=schema_version,
            type_=type_,
            domain=domain,
            status=status,
            business_date=business_date,
            tags=tags,
            data=data,
            envelope=envelope,
            created_at=created_at,
            created_by=created_by,
            edited_at=edited_at,
            edited_by=edited_by,
            edit_count=edit_count,
            source=source,
            audit=audit,
            pipeline=pipeline,
            record=record,
            business=business,
            source_model=source_model,
            source_system=source_system,
        )

        record_out.additional_properties = d
        return record_out

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
