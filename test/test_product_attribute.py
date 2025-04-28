import random

from woo_py.models.product_attribute import ProductAttribute, AttributeType
from woo_py.woo import Woo


def test_product_attribute_methods(woo: Woo, random_str: str):
    # Create a product attribute
    new_attribute = ProductAttribute(
        name=f"Test Attribute {random_str}",
        type=AttributeType.SELECT,
        terms=["Small", "Medium", "Large"]
    )

    created_attribute = woo.create_product_attribute(new_attribute)
    assert created_attribute.id is not None
    assert created_attribute.name == new_attribute.name

    # Get the attribute
    found_attribute = woo.get_product_attribute(created_attribute.id)
    assert found_attribute is not None
    assert found_attribute.id == created_attribute.id

    # Update the attribute
    found_attribute.name = f"Updated Attribute {random_str}"
    updated_attribute = woo.update_product_attribute(found_attribute.id, found_attribute)
    assert updated_attribute.id == found_attribute.id
    assert updated_attribute.name == f"Updated Attribute {random_str}"

    # List attributes
    all_attributes = woo.list_product_attributes()
    assert len(all_attributes) > 0
    assert updated_attribute.id in [attr.id for attr in all_attributes]

    # Delete the attribute
    woo.delete_product_attribute(updated_attribute.id)
    assert woo.get_product_attribute(updated_attribute.id) is None