from datetime import datetime
from pydantic import BaseModel
from typing import Any, Dict, List


class SalesReport(BaseModel):
    total_sales: str | None = None
    net_sales: str | None = None
    average_sales: str | None = None
    total_orders: int | None = None
    total_items: int | None = None
    total_tax: str | None = None
    total_shipping: str | None = None
    total_refunds: int | None = None
    total_discount: int | None = None
    total_customers: int | None = None


class TopSellersReport(BaseModel):
    product_id: int | None = None
    name: str | None = None
    quantity: int | None = None