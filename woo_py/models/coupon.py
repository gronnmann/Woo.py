from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from woo_py.models import MetaData


class DiscountType(str, Enum):
    PERCENT = "percent"
    FIXED_CART = "fixed_cart"
    FIXED_PRODUCT = "fixed_product"


class Coupon(BaseModel):
    id: int | None = None
    code: str
    amount: str | None = None
    date_created: datetime | None = None
    date_created_gmt: datetime | None = None
    date_modified: datetime | None = None
    date_modified_gmt: datetime | None = None
    discount_type: DiscountType | None = DiscountType.FIXED_CART
    description: str | None = None
    date_expires: datetime | None = None
    date_expires_gmt: datetime | None = None
    usage_count: int | None = None
    individual_use: bool | None = False
    product_ids: list[int] = []
    excluded_product_ids: list[int] = []
    usage_limit: int | None = None
    usage_limit_per_user: int | None = None
    limit_usage_to_x_items: int | None = None
    free_shipping: bool | None = False
    product_categories: list[int] = []
    excluded_product_categories: list[int] = []
    exclude_sale_items: bool | None = False
    minimum_amount: int | None = None
    maximum_amount: int | None = None
    email_restrictions: list[str] = []
    used_by: list[int | str] = []
    meta_data: list[MetaData] = []
