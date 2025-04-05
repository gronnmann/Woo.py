import random

from woo_py.models.product_category import ProductCategory
from woo_py.woo import Woo


def test_product_category_methods(woo: Woo, random_str: str):
    # Create a product category
    new_category = ProductCategory(
        name=f"Test Category {random_str}",
        description="Test category for API tests"
    )

    created_category = woo.create_product_category(new_category)
    assert created_category.id is not None
    assert created_category.name == new_category.name

    # Get the category
    found_category = woo.get_product_category(created_category.id)
    assert found_category is not None
    assert found_category.id == created_category.id

    # Update the category
    found_category.description = "Updated test category description"
    updated_category = woo.update_product_category(found_category.id, found_category)
    assert updated_category.id == found_category.id
    assert updated_category.description == "Updated test category description"

    # List categories
    all_categories = woo.list_product_categories(include=[updated_category.id])
    assert len(all_categories) > 0
    assert updated_category.id in [cat.id for cat in all_categories]

    # Delete the category
    woo.delete_product_category(updated_category.id, force=True)
    assert woo.get_product_category(updated_category.id) is None