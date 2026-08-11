import datetime as dt
from typing import Any

from pydantic import BaseModel, Field, field_validator


# --------------------------------------------------------------------------- #
# Envelope models — domain-agnostic metadata, validated at the API boundary
# --------------------------------------------------------------------------- #
class SourceIn(BaseModel):
    document_id: str | None = None
    filename: str | None = None
    file_type: str | None = None
    thumbnail_base64: str | None = None
    page: int | None = Field(default=None, ge=1)
    extracted_at: dt.datetime | None = None
    model: str | None = None
    source_system: str | None = None


class AuditIn(BaseModel):
    created_at: dt.datetime | None = None
    created_by: str | None = None
    edited_at: dt.datetime | None = None
    edited_by: str | None = None
    edit_count: int | None = Field(default=None, ge=0)
    status: str | None = None
    raw_ref: str | None = None


class PipelineIn(BaseModel):
    run_id: str | None = None
    batch_id: str | None = None
    version: str | None = None


class ValidationIn(BaseModel):
    status: str | None = Field(default=None, pattern=r"^(accepted|rejected|quarantined)$")
    warnings: list[str] | None = None


class RecordIn(BaseModel):
    validation: ValidationIn | None = None


class BusinessIn(BaseModel):
    date: dt.date | None = None
    tags: list[str] | None = None
    domain: str | None = None
    is_duplicate: bool | None = None
    coverage: float | None = Field(default=None, ge=0, le=1)


class RecordCreate(BaseModel):
    id: str | None = Field(default=None, max_length=36)
    schema_version: str = "1.0"
    type: str = Field(min_length=1, max_length=64)
    source: SourceIn | None = None
    audit: AuditIn | None = None
    pipeline: PipelineIn | None = None
    record: RecordIn | None = None
    business: BusinessIn | None = None
    data: dict[str, Any]

    @field_validator("id")
    @classmethod
    def _id_chars(cls, v: str | None) -> str | None:
        if v and not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError("id must be alphanumeric, dash or underscore")
        return v


class RecordPatch(BaseModel):
    data: dict[str, Any] | None = None
    business: BusinessIn | None = None
    status: str | None = Field(default=None, pattern=r"^(raw|edited|verified)$")


# --------------------------------------------------------------------------- #
# Response models
# --------------------------------------------------------------------------- #
class RecordOut(BaseModel):
    id: str
    schema_version: str
    type: str
    domain: str | None
    status: str
    business_date: dt.date | None
    tags: list[str] | None
    source: SourceIn | None = None
    audit: AuditIn | None = None
    pipeline: PipelineIn | None = None
    record: RecordIn | None = None
    business: BusinessIn | None = None
    data: dict[str, Any]
    envelope: dict[str, Any]
    created_at: dt.datetime
    created_by: str
    edited_at: dt.datetime | None
    edited_by: str | None
    edit_count: int
    source_model: str | None = None
    source_system: str | None = None


class PageOut(BaseModel):
    items: list[RecordOut]
    page: int
    page_size: int
    total: int
    total_pages: int


class AuditEventOut(BaseModel):
    id: int
    action: str
    actor: str
    at: dt.datetime
    snapshot: dict[str, Any]


class ErrorOut(BaseModel):
    error: dict[str, Any]


# --------------------------------------------------------------------------- #
# Romdoul Data Sharing schemas
# --------------------------------------------------------------------------- #
class OrganizationIn(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    org_type: str = Field(default="other", max_length=32)
    contact: dict[str, Any] | None = None


class OrganizationOut(BaseModel):
    id: int
    name: str
    org_type: str
    contact: dict[str, Any] | None = None
    created_at: dt.datetime


class CategoryIn(BaseModel):
    parent_id: int | None = None
    name: str = Field(min_length=1, max_length=128)
    description: str | None = None
    sort: int = 0


class CategoryOut(BaseModel):
    id: int
    parent_id: int | None = None
    name: str
    description: str | None = None
    sort: int
    created_at: dt.datetime


class CollectionIn(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    description: str | None = None
    organization_id: int | None = None


class CollectionOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    organization_id: int | None = None
    created_at: dt.datetime


class DatasetIn(BaseModel):
    id: str | None = Field(default=None, max_length=36)
    record_id: str | None = None
    name: str = Field(min_length=1, max_length=256)
    description: str | None = None
    organization_id: int | None = None
    category_id: int | None = None
    collection_id: int | None = None
    coverage_start: dt.date | None = None
    coverage_end: dt.date | None = None
    frequency: str | None = None
    url: str | None = None
    file_name: str | None = None
    file_size: int | None = None
    file_type: str | None = None
    file_base64: str | None = None


class DatasetOut(BaseModel):
    id: str
    record_id: str | None = None
    name: str
    description: str | None = None
    organization_id: int | None = None
    category_id: int | None = None
    collection_id: int | None = None
    coverage_start: dt.date | None = None
    coverage_end: dt.date | None = None
    frequency: str | None = None
    url: str | None = None
    status: str
    published_at: dt.datetime | None = None
    file_name: str | None = None
    file_size: int | None = None
    file_type: str | None = None
    file_base64: str | None = None
    created_at: dt.datetime
    updated_at: dt.datetime | None = None


class DatasetPageOut(BaseModel):
    items: list[DatasetOut]
    page: int
    page_size: int
    total: int
    total_pages: int


class AuditEventGlobalOut(BaseModel):
    id: int
    actor: str
    action: str
    entity_type: str
    entity_id: str | None = None
    detail: dict[str, Any] | None = None
    at: dt.datetime


class SettingIn(BaseModel):
    key: str = Field(min_length=1, max_length=64)
    value: dict[str, Any] | None = None


class SettingOut(BaseModel):
    key: str
    value: dict[str, Any] | None = None
    updated_at: dt.datetime


class PasswordChangeIn(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8)
