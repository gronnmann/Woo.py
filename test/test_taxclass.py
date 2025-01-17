from woo_py.models.tax_class import TaxClass
from woo_py.woo import Woo


def test_tax_class_methods(woo: Woo, random_str: str):
    new_tax_class = TaxClass(
        slug=f"test-tax-class-{random_str.lower()}",  # slug is optional
        name=f"Test Tax Class {random_str}",
    )

    created_tax_class = woo.create_tax_class(new_tax_class)
    assert created_tax_class.slug == new_tax_class.slug
    assert created_tax_class.name == new_tax_class.name

    all_tax_classes = woo.list_tax_classes()
    assert len(all_tax_classes) > 0
    assert created_tax_class.slug in [tax_class.slug for tax_class in all_tax_classes]

    woo.delete_tax_class(created_tax_class.slug, force=True)

    all_tax_classes = woo.list_tax_classes()
    assert created_tax_class.slug not in [tax_class.slug for tax_class in all_tax_classes]
