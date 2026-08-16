from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.business_in import BusinessIn
    from ..models.record_patch_data_type_0 import RecordPatchDataType0


T = TypeVar("T", bound="RecordPatch")


@_attrs_define
class RecordPatch:
    """
    Attributes:
        data (None | RecordPatchDataType0 | Unset):
        business (BusinessIn | None | Unset):
        status (None | str | Unset):
    """

    data: None | RecordPatchDataType0 | Unset = UNSET
    business: BusinessIn | None | Unset = UNSET
    status: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.business_in import BusinessIn
        from ..models.record_patch_data_type_0 import RecordPatchDataType0

        data: dict[str, Any] | None | Unset
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, RecordPatchDataType0):
            data = self.data.to_dict()
        else:
            data = self.data

        business: dict[str, Any] | None | Unset
        if isinstance(self.business, Unset):
            business = UNSET
        elif isinstance(self.business, BusinessIn):
            business = self.business.to_dict()
        else:
            business = self.business

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if business is not UNSET:
            field_dict["business"] = business
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.business_in import BusinessIn
        from ..models.record_patch_data_type_0 import RecordPatchDataType0

        d = dict(src_dict)

        def _parse_data(data: object) -> None | RecordPatchDataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = RecordPatchDataType0.from_dict(data)

                return data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RecordPatchDataType0 | Unset, data)

        data = _parse_data(d.pop("data", UNSET))

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

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        record_patch = cls(
            data=data,
            business=business,
            status=status,
        )

        record_patch.additional_properties = d
        return record_patch

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
