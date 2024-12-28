import datetime

from pydantic import BaseModel
from typing import List, Optional

from pydantic_changedetect import ChangeDetectionMixin

from woo_py.models import MetaData, LineItem, TaxLine, ShippingLine, FeeLine


class OrderRefund(ChangeDetectionMixin, BaseModel):
    id: int | None = None  # Unique identifier for the resource, read-only.
    date_created: datetime.datetime | None = (
        None  # Date the order refund was created, in the site's timezone, read-only.
    )
    date_created_gmt: datetime.datetime | None = (
        None  # Date the order refund was created, as GMT, read-only.
    )
    amount: str | None = None  # Total refund amount, optional.
    reason: str | None = None  # Reason for refund.
    refunded_by: int | None = None  # User ID of user who created the refund.
    refunded_payment: bool | None = (
        None  # If the payment was refunded via the API, read-only.
    )
    meta_data: List[MetaData] = []  # Meta data.
    line_items: List[LineItem] = []  # Line items data.
    tax_lines: List[TaxLine] = []  # Tax lines data, read-only.
    shipping_lines: List[ShippingLine] = []  # Shipping lines data.
    fee_lines: List[FeeLine] = []  # Fee lines data.
    api_refund: bool = (
        True  # When true, the payment gateway API is used to generate the refund, write-only.
    )
    api_restock: bool = (
        True  # When true, the selected line items are restocked, write-only.
    )
