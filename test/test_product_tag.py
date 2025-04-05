import random

from woo_py.models.product_tag import ProductTag
from woo_py.woo import Woo


def test_product_tag_methods(woo: Woo, random_str: str):
    # Create a product tag
    new_tag = ProductTag(
        name=f"Test Tag {random_str}",
        description="Test tag for API tests"
    )

    created_tag = woo.create_product_tag(new_tag)
    assert created_tag.id is not None
    assert created_tag.name == new_tag.name

    # Get the tag
    found_tag = woo.get_product_tag(created_tag.id)
    assert found_tag is not None
    assert found_tag.id == created_tag.id

    # Update the tag
    found_tag.description = "Updated test tag description"
    updated_tag = woo.update_product_tag(found_tag.id, found_tag)
    assert updated_tag.id == found_tag.id
    assert updated_tag.description == "Updated test tag description"

    # List tags
    all_tags = woo.list_product_tags(include=[updated_tag.id])
    assert len(all_tags) > 0
    assert updated_tag.id in [tag.id for tag in all_tags]

    # Delete the tag
    woo.delete_product_tag(updated_tag.id, force=True)
    assert woo.get_product_tag(updated_tag.id) is None