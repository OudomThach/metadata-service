from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.capture_ocr_in_pipeline_type_0 import CaptureOcrInPipelineType0
    from ..models.capture_ocr_in_result_type_0 import CaptureOcrInResultType0
    from ..models.capture_ocr_in_source_type_0 import CaptureOcrInSourceType0


T = TypeVar("T", bound="CaptureOcrIn")


@_attrs_define
class CaptureOcrIn:
    """
    Attributes:
        document_name (str):
        full_text (str | Unset):  Default: ''.
        result (CaptureOcrInResultType0 | None | Unset):
        num_pages (int | Unset):  Default: 1.
        pipeline (CaptureOcrInPipelineType0 | None | Unset):
        source (CaptureOcrInSourceType0 | None | Unset):
    """

    document_name: str
    full_text: str | Unset = ""
    result: CaptureOcrInResultType0 | None | Unset = UNSET
    num_pages: int | Unset = 1
    pipeline: CaptureOcrInPipelineType0 | None | Unset = UNSET
    source: CaptureOcrInSourceType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.capture_ocr_in_pipeline_type_0 import CaptureOcrInPipelineType0
        from ..models.capture_ocr_in_result_type_0 import CaptureOcrInResultType0
        from ..models.capture_ocr_in_source_type_0 import CaptureOcrInSourceType0

        document_name = self.document_name

        full_text = self.full_text

        result: dict[str, Any] | None | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, CaptureOcrInResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        num_pages = self.num_pages

        pipeline: dict[str, Any] | None | Unset
        if isinstance(self.pipeline, Unset):
            pipeline = UNSET
        elif isinstance(self.pipeline, CaptureOcrInPipelineType0):
            pipeline = self.pipeline.to_dict()
        else:
            pipeline = self.pipeline

        source: dict[str, Any] | None | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        elif isinstance(self.source, CaptureOcrInSourceType0):
            source = self.source.to_dict()
        else:
            source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document_name": document_name,
            }
        )
        if full_text is not UNSET:
            field_dict["full_text"] = full_text
        if result is not UNSET:
            field_dict["result"] = result
        if num_pages is not UNSET:
            field_dict["num_pages"] = num_pages
        if pipeline is not UNSET:
            field_dict["pipeline"] = pipeline
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.capture_ocr_in_pipeline_type_0 import CaptureOcrInPipelineType0
        from ..models.capture_ocr_in_result_type_0 import CaptureOcrInResultType0
        from ..models.capture_ocr_in_source_type_0 import CaptureOcrInSourceType0

        d = dict(src_dict)
        document_name = d.pop("document_name")

        full_text = d.pop("full_text", UNSET)

        def _parse_result(data: object) -> CaptureOcrInResultType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = CaptureOcrInResultType0.from_dict(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CaptureOcrInResultType0 | None | Unset, data)

        result = _parse_result(d.pop("result", UNSET))

        num_pages = d.pop("num_pages", UNSET)

        def _parse_pipeline(data: object) -> CaptureOcrInPipelineType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                pipeline_type_0 = CaptureOcrInPipelineType0.from_dict(data)

                return pipeline_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CaptureOcrInPipelineType0 | None | Unset, data)

        pipeline = _parse_pipeline(d.pop("pipeline", UNSET))

        def _parse_source(data: object) -> CaptureOcrInSourceType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_type_0 = CaptureOcrInSourceType0.from_dict(data)

                return source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CaptureOcrInSourceType0 | None | Unset, data)

        source = _parse_source(d.pop("source", UNSET))

        capture_ocr_in = cls(
            document_name=document_name,
            full_text=full_text,
            result=result,
            num_pages=num_pages,
            pipeline=pipeline,
            source=source,
        )

        capture_ocr_in.additional_properties = d
        return capture_ocr_in

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
