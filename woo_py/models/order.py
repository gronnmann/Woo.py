import datetime
from enum import Enum
from typing import List, Union
from pydantic import BaseModel

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


class CouponLine(BaseModel):
    id: int | None = None
    code: str | None = None
    discount: float | None = None
    discount_tax: float | None = None
    meta_data: list[MetaData] | None = None


class Refund(BaseModel):
    id: int | None = None
    reason: str | None = None
    total: float | None = None


class Order(BaseModel):
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
    discount_total: float | None = None
    discount_tax: float | None = None
    shipping_total: float | None = None
    shipping_tax: float | None = None
    cart_tax: float | None = None
    total: float | None = None
    total_tax: float | None = None
    prices_include_tax: bool | None = None
    customer_id: int | None = None
    customer_ip_address: str | None = None
    customer_user_agent: str | None = None
    customer_note: str | None = None
    billing: BillingAddress | None = None
    shipping: ShippingAddress | None = None
    payment_method: int | None = None
    payment_method_title: str | None = None
    transaction_id: int | None = None
    date_paid: datetime.datetime | None = None
    date_paid_gmt: datetime.datetime | None = None
    date_completed: datetime.datetime | None = None
    date_completed_gmt: datetime.datetime | None = None
    cart_hash: str | None = None
    meta_data: List[MetaData] | None = None
    line_items: List[LineItem] | None = None
    tax_lines: List[TaxLine] | None = None
    shipping_lines: List[ShippingLine] | None = None
    fee_lines: List[FeeLine] | None = None
    coupon_lines: List[CouponLine] | None = None
    refunds: List[Refund] | None = None
    set_paid: bool = False
