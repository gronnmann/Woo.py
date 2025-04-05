import datetime
from enum import Enum
from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin

from woo_py.models import Dimensions, MetaData, DownloadProperties


class VariationTaxStatus(str, Enum):
    TAXABLE = "taxable"
    SHIPPING = "shipping"
    NONE = "none"


class VariationStockStatus(str, Enum):
    INSTOCK = "instock"
    OUTOFSTOCK = "outofstock"
    ONBACKORDER = "onbackorder"


class VariationBackorders(str, Enum):
    NO = "no"
    NOTIFY = "notify"
    YES = "yes"


class VariationStatus(str, Enum):
    PUBLISH = "publish"
    PRIVATE = "private"
    DRAFT = "draft"
    PENDING = "pending"


class VariationAttribute(BaseModel):
    id: int | None = None
    name: str | None = None
    option: str | None = None


class VariationImage(BaseModel):
    id: int | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None
    src: str | None = None
    name: str | None = None
    alt: str | None = None


class ProductVariation(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None
    description: str | None = None
    permalink: str | None = None
    sku: str | None = None
    price: str | None = None
    regular_price: str | None = None
    sale_price: str | None = None
    date_on_sale_from: datetime.datetime | None = None
    date_on_sale_from_gmt: datetime.datetime | None = None
    date_on_sale_to: datetime.datetime | None = None
    date_on_sale_to_gmt: datetime.datetime | None = None
    on_sale: bool | None = None
    status: VariationStatus = VariationStatus.PUBLISH
    purchasable: bool | None = None
    virtual: bool = False
    downloadable: bool = False
    downloads: list[DownloadProperties] = []
    download_limit: int = -1
    download_expiry: int = -1
    tax_status: VariationTaxStatus = VariationTaxStatus.TAXABLE
    tax_class: str | None = None
    manage_stock: bool = False
    stock_quantity: int | None = None
    stock_status: VariationStockStatus = VariationStockStatus.INSTOCK
    backorders: VariationBackorders = VariationBackorders.NO
    backorders_allowed: bool | None = None
    backordered: bool | None = None
    weight: str | None = None
    dimensions: Dimensions | None = None
    shipping_class: str | None = None
    shipping_class_id: int | None = None
    image: VariationImage | None = None
    attributes: list[VariationAttribute] = []
    menu_order: int | None = None
    meta_data: list[MetaData] = []