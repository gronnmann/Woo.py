from typing import List
from pydantic import BaseModel, Field
from pydantic_changedetect import ChangeDetectionMixin


class TaxRate(ChangeDetectionMixin, BaseModel):
    """
    Model representing a WooCommerce Tax Rate.
    """

    id: int | None = None
    country: str | None = None
    state: str | None = None
    postcode: str | None = None  # Deprecated as of WooCommerce 5.3
    city: str | None = None  # Deprecated as of WooCommerce 5.3
    postcodes: list[str] | None = None
    cities: list[str] | None = None
    rate: str | None = None
    name: str | None = None
    priority: int | None = None
    compound: bool | None = None
    shipping: bool | None = None
    order: int | None = None
    class_: str | None = Field(None, alias="class")
