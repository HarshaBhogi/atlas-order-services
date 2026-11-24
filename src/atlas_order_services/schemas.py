from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TokenRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=120)


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class CustomerCreate(BaseModel):
    external_ref: str = Field(pattern=r"^[A-Z0-9-]{4,40}$")
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr


class CustomerRead(ApiModel):
    id: int
    external_ref: str
    name: str
    email: EmailStr
    status: str
    created_at: datetime


class ProductRead(ApiModel):
    id: int
    sku: str
    name: str
    description: str
    price_cents: int
    active: bool


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)


class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    items: list[OrderItemCreate] = Field(min_length=1, max_length=25)


class OrderItemRead(ApiModel):
    product_id: int
    quantity: int
    unit_price_cents: int


class OrderRead(ApiModel):
    id: int
    customer_id: int
    status: str
    total_cents: int
    created_at: datetime
    items: list[OrderItemRead]


class DocumentWrite(BaseModel):
    customer_id: int = Field(gt=0)
    content: str = Field(min_length=1, max_length=20_000)
    content_type: str = Field(default="text/plain", max_length=100)


class DocumentRead(ApiModel):
    name: str
    content: str


class CallbackRequest(BaseModel):
    target_url: HttpUrl
    event: str = Field(pattern=r"^[a-z][a-z_.-]{2,80}$")
    payload: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class CallbackReceipt(ApiModel):
    target: str
    event: str
    status: str


class AuditEventRead(ApiModel):
    id: int
    actor: str
    action: str
    correlation_id: str
    details: dict[str, object]
    occurred_at: datetime


class Page[ItemT](ApiModel):
    items: list[ItemT]
    offset: int
    limit: int
    total: int


class ReconcileRequest(BaseModel):
    note: str = Field(min_length=3, max_length=300)

    @field_validator("note")
    @classmethod
    def strip_note(cls, value: str) -> str:
        return value.strip()
