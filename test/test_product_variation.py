import random

from woo_py.models.product import Product, ProductType
from woo_py.models.product_variation import ProductVariation
from woo_py.woo import Woo


def test_product_variation_methods(woo: Woo, random_str: str):
    # First create a variable product as parent
    new_product = Product(
        name=f"Test Variable Product {random_str}",
        type=ProductType.VARIABLE,
        description="Test product for variation tests",
        regular_price="19.99"
    )

    created_product = woo.create_product(new_product)
    assert created_product.id is not None
    assert created_product.type == ProductType.VARIABLE

    try:
        # Create a variation for the product
        new_variation = ProductVariation(
            description=f"Test variation {random_str}",
            regular_price="24.99"
        )

        created_variation = woo.create_product_variation(created_product.id, new_variation)
        assert created_variation.id is not None
        assert created_variation.regular_price == "24.99"

        # Get the variation
        found_variation = woo.get_product_variation(created_product.id, created_variation.id)
        assert found_variation is not None
        assert found_variation.id == created_variation.id

        # Update the variation
        found_variation.regular_price = "29.99"
        updated_variation = woo.update_product_variation(
            created_product.id, found_variation.id, found_variation
        )
        assert updated_variation.id == found_variation.id
        assert updated_variation.regular_price == "29.99"

        # List variations
        all_variations = woo.list_product_variations(created_product.id)
        assert len(all_variations) > 0
        assert updated_variation.id in [var.id for var in all_variations]

        # Delete the variation
        woo.delete_product_variation(created_product.id, updated_variation.id, force=True)
        assert woo.get_product_variation(created_product.id, updated_variation.id) is None

    finally:
        # Clean up the parent product regardless of test outcome
        woo.delete_product(created_product.id, force=True)