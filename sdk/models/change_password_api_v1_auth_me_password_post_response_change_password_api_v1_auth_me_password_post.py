from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar(
    "T",
    bound="ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost",
)


@_attrs_define
class ChangePasswordApiV1AuthMePasswordPostResponseChangePasswordApiV1AuthMePasswordPost:
    """ """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        change_password_api_v1_auth_me_password_post_response_change_password_api_v1_auth_me_password_post = cls()

        change_password_api_v1_auth_me_password_post_response_change_password_api_v1_auth_me_password_post.additional_properties = d
        return change_password_api_v1_auth_me_password_post_response_change_password_api_v1_auth_me_password_post

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
