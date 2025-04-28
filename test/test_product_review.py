import random

from woo_py.models.product import Product
from woo_py.models.product_review import ProductReview
from woo_py.woo import Woo


def test_product_review_methods(woo: Woo, random_str: str):
    # First create a product to review
    new_product = Product(
        name=f"Test Product {random_str}",
        description="Test product for review tests",
        regular_price="29.99"
    )

    created_product = woo.create_product(new_product)
    assert created_product.id is not None

    try:
        # Create a product review
        new_review = ProductReview(
            product_id=created_product.id,
            reviewer=f"Test Reviewer {random_str}",
            reviewer_email=f"test_{random_str}@example.com",
            review="This is a test review for testing the API",
            rating=5
        )

        created_review = woo.create_product_review(new_review)
        assert created_review.id is not None
        assert created_review.rating == 5

        # Get the review
        found_review = woo.get_product_review(created_review.id)
        assert found_review is not None
        assert found_review.id == created_review.id

        # Update the review
        found_review.review = "Updated test review"
        updated_review = woo.update_product_review(found_review.id, found_review)
        assert updated_review.id == found_review.id
        assert updated_review.review == "Updated test review"

        # List reviews
        all_reviews = woo.list_product_reviews(product=created_product.id)
        assert len(all_reviews) > 0
        assert updated_review.id in [rev.id for rev in all_reviews]

        # Delete the review
        woo.delete_product_review(updated_review.id, force=True)
        assert woo.get_product_review(updated_review.id) is None

    finally:
        # Clean up the product regardless of test outcome
        woo.delete_product(created_product.id, force=True)