from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.setting_in_value_type_0 import SettingInValueType0


T = TypeVar("T", bound="SettingIn")


@_attrs_define
class SettingIn:
    """
    Attributes:
        key (str):
        value (None | SettingInValueType0 | Unset):
    """

    key: str
    value: None | SettingInValueType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.setting_in_value_type_0 import SettingInValueType0

        key = self.key

        value: dict[str, Any] | None | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, SettingInValueType0):
            value = self.value.to_dict()
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.setting_in_value_type_0 import SettingInValueType0

        d = dict(src_dict)
        key = d.pop("key")

        def _parse_value(data: object) -> None | SettingInValueType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = SettingInValueType0.from_dict(data)

                return value_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SettingInValueType0 | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        setting_in = cls(
            key=key,
            value=value,
        )

        setting_in.additional_properties = d
        return setting_in

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
