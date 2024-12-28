import json

import pytest
from pydantic import BaseModel

from woo_py.models.coupon import Coupon
from woo_py.models.customer import Customer
from woo_py.models.order import Order
from woo_py.models.order_note import OrderNote
from woo_py.models.order_refund import OrderRefund
from woo_py.models.product import Product
from woo_py.models.webhook import Webhook


def _class_to_snake_case(obj):
    """Converts a python class to snake case"""
    # For example, UserInfo to user_info

    return "".join(
        ["_" + i.lower() if i.isupper() else i for i in obj.__name__]
    ).lstrip("_")

@pytest.mark.parametrize(
    "object",
    [
        Coupon,
        Customer,
        Order,
        OrderNote,
        OrderRefund,
        Product,
        Webhook,
    ],
)
def test_parse_sample_data(object: BaseModel):
    file_name = f"test/sample_data/{_class_to_snake_case(object)}.json"

    with open(file_name) as f:
        data = f.read()

    as_dict = json.loads(data)

    item = object.model_validate(as_dict)