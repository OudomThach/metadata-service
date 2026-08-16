from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_item_result_error_type_0 import BatchItemResultErrorType0


T = TypeVar("T", bound="BatchItemResult")


@_attrs_define
class BatchItemResult:
    """
    Attributes:
        ok (bool):
        id (None | str | Unset):
        error (BatchItemResultErrorType0 | None | Unset):
    """

    ok: bool
    id: None | str | Unset = UNSET
    error: BatchItemResultErrorType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_item_result_error_type_0 import BatchItemResultErrorType0

        ok = self.ok

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        error: dict[str, Any] | None | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, BatchItemResultErrorType0):
            error = self.error.to_dict()
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.batch_item_result_error_type_0 import BatchItemResultErrorType0

        d = dict(src_dict)
        ok = d.pop("ok")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_error(data: object) -> BatchItemResultErrorType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = BatchItemResultErrorType0.from_dict(data)

                return error_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BatchItemResultErrorType0 | None | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        batch_item_result = cls(
            ok=ok,
            id=id,
            error=error,
        )

        batch_item_result.additional_properties = d
        return batch_item_result

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
