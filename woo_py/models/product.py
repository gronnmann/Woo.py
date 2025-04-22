import datetime
from typing import Literal

from pydantic import BaseModel


import datetime
from enum import Enum
from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin

from woo_py.models import Dimensions, DownloadProperties, MetaData


class ProductType(str, Enum):
    SIMPLE = "simple"
    GROUPED = "grouped"
    EXTERNAL = "external"
    VARIABLE = "variable"


class ProductStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PRIVATE = "private"
    PUBLISH = "publish"


class CatalogVisibility(str, Enum):
    VISIBLE = "visible"
    CATALOG = "catalog"
    SEARCH = "search"
    HIDDEN = "hidden"


class ProductTaxStatus(str, Enum):
    TAXABLE = "taxable"
    SHIPPING = "shipping"
    NONE = "none"


class ProductStockStatus(str, Enum):
    INSTOCK = "instock"
    OUTOFSTOCK = "outofstock"
    ONBACKORDER = "onbackorder"


class Backorders(str, Enum):
    NO = "no"
    NOTIFY = "notify"
    YES = "yes"


class ProductCategory(BaseModel):
    id: int
    name: str
    slug: str


class ProductTag(BaseModel):
    id: int
    name: str
    slug: str


class ProductImage(BaseModel):
    id: int
    date_created: datetime.datetime
    date_created_gmt: datetime.datetime
    date_modified: datetime.datetime
    date_modified_gmt: datetime.datetime
    src: str
    name: str
    alt: str


class ProductDefaultAttribute(BaseModel):
    id: int
    name: str
    option: str


class ProductAttribute(BaseModel):
    id: int
    name: str
    position: int
    visible: bool = False
    variation: bool = False
    options: list[ProductDefaultAttribute | str]


class Product(ChangeDetectionMixin, BaseModel):
    id: int | None = None
    name: str | None = None
    slug: str | None = None
    permalink: str | None = None
    date_created: datetime.datetime | None = None
    date_created_gmt: datetime.datetime | None = None
    date_modified: datetime.datetime | None = None
    date_modified_gmt: datetime.datetime | None = None
    type: ProductType = ProductType.SIMPLE
    status: ProductStatus = ProductStatus.PUBLISH
    featured: bool = False
    catalog_visibility: CatalogVisibility = CatalogVisibility.VISIBLE
    description: str | None = None
    short_description: str | None = None
    sku: str | None = None
    price: str | None = None
    regular_price: str | None = None
    sale_price: str | None = None
    date_on_sale_from: datetime.datetime | None = None
    date_on_sale_from_gmt: datetime.datetime | None = None
    date_on_sale_to: datetime.datetime | None = None
    date_on_sale_to_gmt: datetime.datetime | None = None
    price_html: str | None = None
    on_sale: bool | None = None
    purchasable: bool | None = None
    total_sales: int | None = None
    virtual: bool = False
    downloadable: bool = False
    downloads: list[DownloadProperties] = []
    download_limit: int = -1
    download_expiry: int = -1
    external_url: str | None = None
    button_text: str | None = None
    tax_status: ProductTaxStatus = ProductTaxStatus.TAXABLE
    tax_class: str | None = None
    manage_stock: bool = False
    stock_quantity: int | None = None
    stock_status: ProductStockStatus = ProductStockStatus.INSTOCK
    backorders: Backorders = Backorders.NO
    backorders_allowed: bool | None = None
    backordered: bool | None = None
    sold_individually: bool = False
    weight: str | None = None
    dimensions: Dimensions | None = None
    shipping_required: bool | None = None
    shipping_taxable: bool | None = None
    shipping_class: str | None = None
    shipping_class_id: int | None = None
    reviews_allowed: bool = True
    average_rating: str | None = None
    rating_count: int | None = None
    related_ids: list[int] = []
    upsell_ids: list[int] = []
    cross_sell_ids: list[int] = []
    parent_id: int | None = None
    purchase_note: str | None = None
    categories: list[ProductCategory] = []
    tags: list[ProductTag] = []
    images: list[ProductImage] = []
    attributes: list[ProductAttribute] = []
    default_attributes: list[ProductDefaultAttribute] = []
    variations: list[int] = []
    grouped_products: list[int] = []
    menu_order: int | None = None
    meta_data: list[MetaData] = []
