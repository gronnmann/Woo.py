from pydantic import BaseModel
from datetime import datetime

from woo_py.models import MetaData, BillingAddress, ShippingAddress


class Customer(BaseModel):
    id: int | None = None
    date_created: datetime | None = None
    date_created_gmt: datetime | None = None
    date_modified: datetime | None = None
    date_modified_gmt: datetime | None = None
    email: str
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    username: str | None = None
    password: str | None = None
    billing: BillingAddress | None = None
    shipping: ShippingAddress | None = None
    is_paying_customer: bool | None = None
    avatar_url: str | None = None
    meta_data: list[MetaData] = []
