import datetime

from pydantic import BaseModel
from enum import Enum

from pydantic_changedetect import ChangeDetectionMixin


class WebhookStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    DISABLED = "disabled"


class WebhookTopic(str, Enum):
    COUPON_CREATED = "coupon.created"
    COUPON_UPDATED = "coupon.updated"
    COUPON_DELETED = "coupon.deleted"

    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"
    CUSTOMER_DELETED = "customer.deleted"

    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    ORDER_DELETED = "order.deleted"

    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    PRODUCT_DELETED = "product.deleted"


class Webhook(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    name: str | None = None
    status: WebhookStatus = WebhookStatus.ACTIVE
    topic: str | WebhookTopic
    resource: str | None = None
    event: str | None = None
    hooks: list[str] | None = None
    delivery_url: str
    secret: str | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None
