from enum import Enum

from pydantic import BaseModel, ConfigDict
import typing


# Common models
class MetaData(BaseModel):
    id: int | None  # Meta ID (read-only)
    key: str | None  # Meta key
    value: str | list[str] | dict[str, typing.Any] | None  # Meta value


class ShippingAddress(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    address_1: str | None = None
    address_2: str | None = None
    city: str | None = None
    state: str | None = None
    postcode: str | None = None
    country: str | None = None


class BillingAddress(ShippingAddress):
    email: str | None = None
    phone: str | None = None


class TaxLine(BaseModel):
    id: int | None = None  # Item ID, read-only.
    rate_code: str | None = None  # Tax rate code, read-only.
    rate_id: int | None = None  # Tax rate ID, read-only.
    label: str | None = None  # Tax rate label, read-only.
    compound: bool | None = (
        None  # Whether or not this is a compound tax rate, read-only.
    )
    tax_total: float | None = (
        None  # Tax total (not including shipping taxes), read-only.
    )
    shipping_tax_total: str | None = None  # Shipping tax total, read-only.
    meta_data: list[MetaData] = []  # Meta data.


class TaxStatus(str, Enum):
    TAXABLE = "taxable"
    NONE = "none"


class FeeLine(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: int | None = None
    name: str | None = None
    tax_class: str | None = None
    tax_status: TaxStatus
    total: str | None = None
    total_tax: str | None = None
    taxes: list[TaxLine] = []
    meta_data: list[MetaData] = []


class ShippingLine(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: str | None = None
    method_title: str | None = None
    method_id: str | None = None
    total: str | None = None
    total_tax: str | None = None
    taxes: list[TaxLine] = []
    meta_data: list[MetaData] = []


class LineItem(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: int | None = None
    name: str | None = None
    product_id: int | None = None
    variation_id: int | None = None
    quantity: int | None = None
    tax_class: str | None = None
    subtotal: str | None = None
    subtotal_tax: str | None = None
    total: str | None = None
    total_tax: str | None = None
    taxes: list[TaxLine] = []
    meta_data: list[MetaData] = []
    sku: str | None = None
    price: str | None = None


class Dimensions(BaseModel):
    length: str | None = None
    width: str | None = None
    height: str | None = None


class DownloadProperties(BaseModel):
    id: str
    name: str
    file: str


# Import all models
from woo_py.models.coupon import Coupon
from woo_py.models.customer import Customer
from woo_py.models.data import Country, Currency
from woo_py.models.order import Order, OrderStatus
from woo_py.models.order_note import OrderNote
from woo_py.models.order_refund import OrderRefund
from woo_py.models.payment_gateway import PaymentGateway, PaymentGatewaySetting
from woo_py.models.product import (
    Product,
    ProductType,
    ProductStatus,
    ProductCategory as ProductCategoryRef,
    ProductTag as ProductTagRef,
)
from woo_py.models.product_attribute import (
    ProductAttribute,
    AttributeType,
    AttributeOrderBy,
)
from woo_py.models.product_category import ProductCategory, ProductCategoryImage
from woo_py.models.product_review import ProductReview, ReviewStatus
from woo_py.models.product_tag import ProductTag
from woo_py.models.product_variation import ProductVariation, VariationStatus
from woo_py.models.report import SalesReport, TopSellersReport
from woo_py.models.setting import SettingOption
from woo_py.models.tax_class import TaxClass
from woo_py.models.webhook import Webhook, WebhookStatus, WebhookTopic
