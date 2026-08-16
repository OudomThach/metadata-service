from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.validation_in import ValidationIn


T = TypeVar("T", bound="RecordIn")


@_attrs_define
class RecordIn:
    """
    Attributes:
        validation (None | Unset | ValidationIn):
    """

    validation: None | Unset | ValidationIn = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.validation_in import ValidationIn

        validation: dict[str, Any] | None | Unset
        if isinstance(self.validation, Unset):
            validation = UNSET
        elif isinstance(self.validation, ValidationIn):
            validation = self.validation.to_dict()
        else:
            validation = self.validation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if validation is not UNSET:
            field_dict["validation"] = validation

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.validation_in import ValidationIn

        d = dict(src_dict)

        def _parse_validation(data: object) -> None | Unset | ValidationIn:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                validation_type_0 = ValidationIn.from_dict(data)

                return validation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | ValidationIn, data)

        validation = _parse_validation(d.pop("validation", UNSET))

        record_in = cls(
            validation=validation,
        )

        record_in.additional_properties = d
        return record_in

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
