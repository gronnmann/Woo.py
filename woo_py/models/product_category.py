import datetime
from enum import Enum
from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin

from woo_py.models import MetaData


class ProductCategoryDisplay(str, Enum):
    DEFAULT = "default"
    PRODUCTS = "products"
    SUBCATEGORIES = "subcategories"
    BOTH = "both"


class ProductCategoryImage(BaseModel):
    id: int | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None
    src: str | None = None
    name: str | None = None
    alt: str | None = None


class ProductCategory(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    name: str
    slug: str | None = None
    parent: int | None = None
    description: str | None = None
    display: ProductCategoryDisplay | None = ProductCategoryDisplay.DEFAULT
    image: ProductCategoryImage | None = None
    menu_order: int | None = None
    count: int | None = None
