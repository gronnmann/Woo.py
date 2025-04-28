import datetime
from enum import Enum
from typing import List, Union
from pydantic import BaseModel, ConfigDict
from pydantic_changedetect import ChangeDetectionMixin

from woo_py.models import (
    MetaData,
    ShippingLine,
    FeeLine,
    BillingAddress,
    ShippingAddress,
    LineItem,
    TaxLine,
)


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    ON_HOLD = "on-hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    FAILED = "failed"
    TRASH = "trash"
    CHECKOUT_DRAFT = "checkout-draft"


class CouponLine(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: int | None = None
    code: str | None = None
    discount: str | None = None
    discount_tax: str | None = None
    meta_data: list[MetaData] = []


class Refund(BaseModel):
    id: int | None = None
    reason: str | None = None
    total: str | None = None


class Order(ChangeDetectionMixin, BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    id: int | None = None
    parent_id: int | None = None
    number: str | None = None
    order_key: str | None = None
    created_via: str | None = None
    version: str | None = None
    status: OrderStatus | None = None
    currency: str | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None
    discount_total: str | None = None
    discount_tax: str | None = None
    shipping_total: str | None = None
    shipping_tax: str | None = None
    cart_tax: str | None = None
    total: str | None = None
    total_tax: str | None = None
    prices_include_tax: bool | None = None
    customer_id: int | None = None
    customer_ip_address: str | None = None
    customer_user_agent: str | None = None
    customer_note: str | None = None
    billing: BillingAddress | None = None
    shipping: ShippingAddress | None = None
    payment_method: str | None = None
    payment_method_title: str | None = None
    transaction_id: str | None = None
    date_paid: datetime.datetime | None = None
    date_paid_gmt: datetime.datetime | None = None
    date_completed: datetime.datetime | None = None
    date_completed_gmt: datetime.datetime | None = None
    cart_hash: str | None = None
    meta_data: List[MetaData] = []
    line_items: List[LineItem] = []
    tax_lines: List[TaxLine] = []
    shipping_lines: List[ShippingLine] = []
    fee_lines: List[FeeLine] = []
    coupon_lines: List[CouponLine] = []
    refunds: List[Refund] = []
    set_paid: bool = False
