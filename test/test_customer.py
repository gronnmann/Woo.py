import random

from woo_py.models.customer import Customer
from woo_py.woo import Woo


def test_customer_methods(woo: Woo, random_str: str):
    new_customer = Customer(

        email=f"test_{random_str}@example.com",
        first_name="Test",
        last_name="Customer",
        username=f"test_{random_str.lower()}"
    )

    created_customer = woo.create_customer(new_customer)
    assert created_customer.id is not None

    found_customer = woo.get_customer(created_customer.id)
    assert found_customer is not None
    assert found_customer.id == created_customer.id

    found_customer.first_name = "Updated"
    updated_customer = woo.update_customer(found_customer.id, found_customer)
    assert updated_customer.id == found_customer.id

    all_customers = woo.list_customers(include=[updated_customer.id])
    assert len(all_customers) > 0
    assert updated_customer.id in [cust.id for cust in all_customers]

    woo.delete_customer(updated_customer.id, force=True)
    assert woo.get_customer(updated_customer.id) is None