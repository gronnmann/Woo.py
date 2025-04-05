from pydantic import BaseModel

from woo_py.models.coupon import Coupon
from woo_py.models.customer import Customer
from woo_py.models.product import Product
from woo_py.models.product_variation import ProductVariation
from woo_py.models.product_category import ProductCategory
from woo_py.models.product_tag import ProductTag
from woo_py.models.product_attribute import ProductAttribute
from woo_py.models.product_review import ProductReview
from woo_py.models.payment_gateway import PaymentGateway
from woo_py.models.report import SalesReport, TopSellersReport
from woo_py.models.setting import SettingOption
from woo_py.models.data import Country, Currency
from woo_py.models.tax_class import TaxClass
from woo_py.models.webhook import Webhook
import typing as t

from woo_py.api import API

ContextType = t.Literal["view", "edit"]
OrderType = t.Literal["asc", "desc"]


class Woo:
    """
    Represents the main interface for accessing the API.
    """

    api_object: API

    def __init__(self, api_object: API) -> None:
        self.api_object = api_object

    # Coupons
    def create_coupon(self, coupon: Coupon) -> Coupon:
        """
        Creates a coupon.
        :param coupon: Coupon object
        :return: the created coupon
        """
        return self.api_object.post("coupons", coupon)

    def get_coupon(self, coupon_id: int) -> Coupon | None:
        """
        Gets a coupon by its ID.
        :param coupon_id: id of the coupon
        :return:
        """
        return self.api_object.get(f"coupons/{coupon_id}", Coupon)

    def list_coupons(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int = 0,
            order: OrderType = "asc",
            orderby: t.Literal[
                "date", "modified", "id", "include", "title", "slug"
            ] = "date",
            code: str | None = None,
    ) -> list[Coupon]:
        """
        Lists all coupons.
        """

        return self.api_object.get_all(
            "coupons",
            Coupon,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            after=after,
            before=before,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
            code=code,
        )

    def update_coupon(self, coupon_id: int, coupon: Coupon) -> Coupon:
        """
        Updates a coupon by its ID.
        :param coupon_id: id of the coupon
        :param coupon: Coupon object
        :return:
        """
        return self.api_object.put(f"coupons/{coupon_id}", coupon)

    def delete_coupon(self, coupon_id: int) -> None:
        """
        Deletes a coupon by its ID.
        :param coupon_id: id of the coupon
        :return: None
        """
        self.api_object.delete(f"coupons/{coupon_id}")

    # Webhooks

    def create_webhook(self, webhook: Webhook) -> Webhook:
        """
        Creates a webhook.
        :param webhook: Webhook object
        :return: the created webhook
        """
        return self.api_object.post("webhooks", webhook)

    def get_webhook(self, webhook_id: int) -> Webhook | None:
        """
        Gets a webhook by its ID.
        :param webhook_id: id of the webhook
        :return:
        """
        return self.api_object.get(f"webhooks/{webhook_id}", Webhook)

    def delete_webhook(self, webhook_id: int, force: bool = False) -> None:
        """
        Deletes a webhook by its ID.
        :param webhook_id: id of the webhook
        :param force: when True, the webhook will be permanently deleted
        :return: None
        """
        return self.api_object.delete(f"webhooks/{webhook_id}", force=force)

    def list_webhooks(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = "desc",
            orderby: t.Literal["date", "id", "title"] = "date",
            status: t.Literal["all", "active", "paused", "disabled", "all"] = "all",
    ) -> list[Webhook]:
        """
        Lists all webhooks.
        :return: list of Webhook objects
        """
        params = {
            "context": context,
            "page": page,
            "per_page": per_page,
            "search": search,
            "after": after,
            "before": before,
            "exclude": exclude,
            "include": include,
            "offset": offset,
            "order": order,
            "orderby": orderby,
            "status": status,
        }
        return self.api_object.get_all(
            "webhooks/",
            Webhook,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            after=after,
            before=before,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
            status=status,
        )

    def update_webhook(self, webhook_id: int, webhook: Webhook) -> Webhook:
        """
        Updates a webhook by its ID.
        :param webhook_id: id of the webhook
        :param webhook_edit: edit object
        :return:
        """
        return self.api_object.put(f"webhooks/{webhook_id}", webhook)

    # Customers

    def create_customer(self, customer: Customer) -> BaseModel:
        """
        Creates a customer.
        :param customer: Customer object
        :return: the created customer
        """
        return self.api_object.post("customers", customer)

    def get_customer(self, customer_id: int) -> BaseModel | None:
        """
        Gets a customer by its ID.
        :param customer_id: id of the customer
        :return:
        """
        return self.api_object.get(f"customers/{customer_id}", Customer)

    def list_customers(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = "asc",
            orderby: t.Literal["id", "include", "name", "registered_date"] = "name",
            email: str | None = None,
            role: t.Literal[
                "all",
                "administrator",
                "editor",
                "author",
                "contributor",
                "subscriber",
                "customer",
                "shop_manager",
            ] = "customer",
    ) -> list[Customer]:
        """
        Lists all customers
        """

        return self.api_object.get_all(
            "customers",
            Customer,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
            email=email,
            role=role,
        )

    def update_customer(self, customer_id: int, customer: Customer) -> BaseModel:
        """
        Updates a customer by its ID.
        :param customer_id: id of the customer
        :param customer: Customer object
        :return:
        """
        return self.api_object.put(f"customers/{customer_id}", customer)

    def delete_customer(
            self, customer_id: int, force: bool, reassign: int | None = None
    ) -> None:
        """
        Deletes a customer by its ID.
        :param customer_id: id of the customer
        :param force: required to be True, as customer does not support trashing
        :param reassign: id of the customer to reassign the customer's posts to
        :return: None
        """

        self.api_object.delete(
            f"customers/{customer_id}", force=force, reassign=reassign
        )

    # Tax classes
    def create_tax_class(self, tax_class: TaxClass) -> BaseModel:
        """
        Creates a tax class.
        :param tax_class: Tax class object
        :return: the created tax class
        """
        return self.api_object.post("taxes/classes", tax_class)

    def list_tax_classes(self) -> list[TaxClass]:
        """
        Lists all tax classes.
        """
        return self.api_object.get_all("taxes/classes", TaxClass)

    def delete_tax_class(self, slug: str, force: bool) -> None:
        """
        Deletes a tax class by its ID.
        :param tax_class_id: id of the tax class
        :param force: required to be True, as tax class does not support trashing
        :return: None
        """
        self.api_object.delete(f"taxes/classes/{slug}", force=force)

    # Products
    def create_product(self, product: Product) -> Product:
        """
        Creates a product.
        :param product: Product object
        :return: the created product
        """
        return self.api_object.post("products", product)

    def get_product(self, product_id: int) -> Product | None:
        """
        Gets a product by its ID.
        :param product_id: id of the product
        :return: Product object or None if not found
        """
        return self.api_object.get(f"products/{product_id}", Product)

    def list_products(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = "desc",
            orderby: t.Literal[
                "date", "id", "include", "title", "slug", "price", "popularity", "rating"
            ] = "date",
            category: str | None = None,
            tag: str | None = None,
            status: t.Literal["any", "draft", "pending", "private", "publish"] = "any",
            type: t.Literal["simple", "grouped", "external", "variable"] = "simple",
            featured: bool | None = None,
            sku: str | None = None,
    ) -> list[Product]:
        """
        Lists all products.
        :return: list of Product objects
        """
        return self.api_object.get_all(
            "products",
            Product,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            after=after,
            before=before,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
            category=category,
            tag=tag,
            status=status,
            type=type,
            featured=featured,
            sku=sku,
        )

    def update_product(self, product_id: int, product: Product) -> Product:
        """
        Updates a product by its ID.
        :param product_id: id of the product
        :param product: Product object with updates
        :return: updated Product object
        """
        return self.api_object.put(f"products/{product_id}", product)

    def delete_product(self, product_id: int, force: bool = False) -> None:
        """
        Deletes a product by its ID.
        :param product_id: id of the product
        :param force: when True, the product will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"products/{product_id}", force=force)

    # Product Variations
    def create_product_variation(self, product_id: int, variation: ProductVariation) -> ProductVariation:
        """
        Creates a product variation.
        :param product_id: id of the parent product
        :param variation: ProductVariation object
        :return: the created variation
        """
        return self.api_object.post(f"products/{product_id}/variations", variation)

    def get_product_variation(self, product_id: int, variation_id: int) -> ProductVariation | None:
        """
        Gets a product variation by its ID.
        :param product_id: id of the parent product
        :param variation_id: id of the variation
        :return: ProductVariation object or None if not found
        """
        return self.api_object.get(f"products/{product_id}/variations/{variation_id}", ProductVariation)

    def list_product_variations(
            self,
            product_id: int,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = "desc",
            orderby: t.Literal["date", "id", "include", "title", "slug"] = "date",
    ) -> list[ProductVariation]:
        """
        Lists all variations for a product.
        :param product_id: id of the parent product
        :return: list of ProductVariation objects
        """
        return self.api_object.get_all(
            f"products/{product_id}/variations",
            ProductVariation,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            after=after,
            before=before,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
        )

    def update_product_variation(
            self, product_id: int, variation_id: int, variation: ProductVariation
    ) -> ProductVariation:
        """
        Updates a product variation by its ID.
        :param product_id: id of the parent product
        :param variation_id: id of the variation
        :param variation: ProductVariation object with updates
        :return: updated ProductVariation object
        """
        return self.api_object.put(f"products/{product_id}/variations/{variation_id}", variation)

    def delete_product_variation(
            self, product_id: int, variation_id: int, force: bool = False
    ) -> None:
        """
        Deletes a product variation by its ID.
        :param product_id: id of the parent product
        :param variation_id: id of the variation
        :param force: when True, the variation will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"products/{product_id}/variations/{variation_id}", force=force)

    # Product Categories
    def create_product_category(self, category: ProductCategory) -> ProductCategory:
        """
        Creates a product category.
        :param category: ProductCategory object
        :return: the created category
        """
        return self.api_object.post("products/categories", category)

    def get_product_category(self, category_id: int) -> ProductCategory | None:
        """
        Gets a product category by its ID.
        :param category_id: id of the category
        :return: ProductCategory object or None if not found
        """
        return self.api_object.get(f"products/categories/{category_id}", ProductCategory)

    def list_product_categories(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            order: OrderType = "asc",
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = "name",
            hide_empty: bool = False,
            parent: int | None = None,
            product: int | None = None,
            slug: str | None = None,
    ) -> list[ProductCategory]:
        """
        Lists all product categories.
        :return: list of ProductCategory objects
        """
        return self.api_object.get_all(
            "products/categories",
            ProductCategory,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            exclude=exclude,
            include=include,
            order=order,
            orderby=orderby,
            hide_empty=hide_empty,
            parent=parent,
            product=product,
            slug=slug,
        )

    def update_product_category(
            self, category_id: int, category: ProductCategory
    ) -> ProductCategory:
        """
        Updates a product category by its ID.
        :param category_id: id of the category
        :param category: ProductCategory object with updates
        :return: updated ProductCategory object
        """
        return self.api_object.put(f"products/categories/{category_id}", category)

    def delete_product_category(self, category_id: int, force: bool = False) -> None:
        """
        Deletes a product category by its ID.
        :param category_id: id of the category
        :param force: when True, the category will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"products/categories/{category_id}", force=force)

    # Product Tags
    def create_product_tag(self, tag: ProductTag) -> ProductTag:
        """
        Creates a product tag.
        :param tag: ProductTag object
        :return: the created tag
        """
        return self.api_object.post("products/tags", tag)

    def get_product_tag(self, tag_id: int) -> ProductTag | None:
        """
        Gets a product tag by its ID.
        :param tag_id: id of the tag
        :return: ProductTag object or None if not found
        """
        return self.api_object.get(f"products/tags/{tag_id}", ProductTag)

    def list_product_tags(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = "asc",
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = "name",
            hide_empty: bool = False,
            product: int | None = None,
            slug: str | None = None,
    ) -> list[ProductTag]:
        """
        Lists all product tags.
        :return: list of ProductTag objects
        """
        return self.api_object.get_all(
            "products/tags",
            ProductTag,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
            hide_empty=hide_empty,
            product=product,
            slug=slug,
        )

    def update_product_tag(self, tag_id: int, tag: ProductTag) -> ProductTag:
        """
        Updates a product tag by its ID.
        :param tag_id: id of the tag
        :param tag: ProductTag object with updates
        :return: updated ProductTag object
        """
        return self.api_object.put(f"products/tags/{tag_id}", tag)

    def delete_product_tag(self, tag_id: int, force: bool = False) -> None:
        """
        Deletes a product tag by its ID.
        :param tag_id: id of the tag
        :param force: when True, the tag will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"products/tags/{tag_id}", force=force)

    # Product Attributes
    def create_product_attribute(self, attribute: ProductAttribute) -> ProductAttribute:
        """
        Creates a product attribute.
        :param attribute: ProductAttribute object
        :return: the created attribute
        """
        return self.api_object.post("products/attributes", attribute)

    def get_product_attribute(self, attribute_id: int) -> ProductAttribute | None:
        """
        Gets a product attribute by its ID.
        :param attribute_id: id of the attribute
        :return: ProductAttribute object or None if not found
        """
        return self.api_object.get(f"products/attributes/{attribute_id}", ProductAttribute)

    def list_product_attributes(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            order: OrderType = "asc",
            orderby: t.Literal["id", "name", "slug", "type", "order_by"] = "name",
    ) -> list[ProductAttribute]:
        """
        Lists all product attributes.
        :return: list of ProductAttribute objects
        """
        return self.api_object.get_all(
            "products/attributes",
            ProductAttribute,
            context=context,
            page=page,
            per_page=per_page,
            order=order,
            orderby=orderby,
        )

    def update_product_attribute(
            self, attribute_id: int, attribute: ProductAttribute
    ) -> ProductAttribute:
        """
        Updates a product attribute by its ID.
        :param attribute_id: id of the attribute
        :param attribute: ProductAttribute object with updates
        :return: updated ProductAttribute object
        """
        return self.api_object.put(f"products/attributes/{attribute_id}", attribute)

    def delete_product_attribute(self, attribute_id: int, force: bool = True) -> None:
        """
        Deletes a product attribute by its ID.
        :param attribute_id: id of the attribute
        :param force: when True, the attribute will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"products/attributes/{attribute_id}", force=force)

    # Product Reviews
    def create_product_review(self, review: ProductReview) -> ProductReview:
        """
        Creates a product review.
        :param review: ProductReview object
        :return: the created review
        """
        return self.api_object.post("products/reviews", review)

    def get_product_review(self, review_id: int) -> ProductReview | None:
        """
        Gets a product review by its ID.
        :param review_id: id of the review
        :return: ProductReview object or None if not found
        """
        return self.api_object.get(f"products/reviews/{review_id}", ProductReview)

    def list_product_reviews(
            self,
            context: ContextType = "view",
            page: int = 1,
            per_page: int = 10,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = "desc",
            orderby: t.Literal["date", "date_gmt", "id", "include", "product", "rating"] = "date",
            reviewer: str | None = None,
            reviewer_email: str | None = None,
            product: int | None = None,
            status: t.Literal["approved", "hold", "spam", "unspam", "trash", "untrash"] = "approved",
    ) -> list[ProductReview]:
        """
        Lists all product reviews.
        :return: list of ProductReview objects
        """
        return self.api_object.get_all(
            "products/reviews",
            ProductReview,
            context=context,
            page=page,
            per_page=per_page,
            search=search,
            after=after,
            before=before,
            exclude=exclude,
            include=include,
            offset=offset,
            order=order,
            orderby=orderby,
            reviewer=reviewer,
            reviewer_email=reviewer_email,
            product=product,
            status=status,
        )

    def update_product_review(
            self, review_id: int, review: ProductReview
    ) -> ProductReview:
        """
        Updates a product review by its ID.
        :param review_id: id of the review
        :param review: ProductReview object with updates
        :return: updated ProductReview object
        """
        return self.api_object.put(f"products/reviews/{review_id}", review)

    def delete_product_review(self, review_id: int, force: bool = False) -> None:
        """
        Deletes a product review by its ID.
        :param review_id: id of the review
        :param force: when True, the review will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"products/reviews/{review_id}", force=force)

    # Payment Gateways
    def list_payment_gateways(self) -> list[PaymentGateway]:
        """
        Lists all payment gateways.
        :return: list of PaymentGateway objects
        """
        return self.api_object.get_all(
            "payment_gateways",
            PaymentGateway,
        )

    def get_payment_gateway(self, gateway_id: str) -> PaymentGateway | None:
        """
        Gets a payment gateway by its ID.
        :param gateway_id: id of the payment gateway
        :return: PaymentGateway object or None if not found
        """
        return self.api_object.get(f"payment_gateways/{gateway_id}", PaymentGateway)

    def update_payment_gateway(
            self, gateway_id: str, gateway: PaymentGateway
    ) -> PaymentGateway:
        """
        Updates a payment gateway by its ID.
        :param gateway_id: id of the payment gateway
        :param gateway: PaymentGateway object with updates
        :return: updated PaymentGateway object
        """
        return self.api_object.put(f"payment_gateways/{gateway_id}", gateway)


    # Data endpoints
    def get_countries(self) -> list[Country]:
        """
        Gets all countries.
        :return: list of Country objects
        """
        return self.api_object.get_all("data/countries", Country)

    def get_country(self, country_code: str) -> Country | None:
        """
        Gets a country by its code.
        :param country_code: two-character country code
        :return: Country object or None if not found
        """
        return self.api_object.get(f"data/countries/{country_code}", Country)

    def get_currencies(self) -> list[Currency]:
        """
        Gets all currencies.
        :return: list of Currency objects
        """
        return self.api_object.get_all("data/currencies", Currency)

    def get_currency(self, currency_code: str) -> Currency | None:
        """
        Gets a currency by its code.
        :param currency_code: three-character currency code
        :return: Currency object or None if not found
        """
        return self.api_object.get(f"data/currencies/{currency_code}", Currency)

    # Reports
    def get_sales_report(
        self,
        period: t.Literal["week", "month", "last_month", "year"] = "week",
        date_min: str | None = None,
        date_max: str | None = None,
    ) -> SalesReport | None:
        """
        Gets the sales report.
        :param period: The period of sales to return
        :param date_min: The start date for the report (ISO 8601 format)
        :param date_max: The end date for the report (ISO 8601 format)
        :return: SalesReport object or None if not found
        """
        params: dict[str, str] = {"period": period}
        if date_min:
            params["date_min"] = date_min
        if date_max:
            params["date_max"] = date_max
            
        return self.api_object.get("reports/sales", SalesReport, **params)

    def get_top_sellers_report(
        self,
        period: t.Literal["week", "month", "last_month", "year"] = "week",
        date_min: str | None = None,
        date_max: str | None = None,
    ) -> list[TopSellersReport]:
        """
        Gets the top sellers report.
        :param period: The period of sales to return
        :param date_min: The start date for the report (ISO 8601 format)
        :param date_max: The end date for the report (ISO 8601 format)
        :return: list of TopSellersReport objects
        """
        params: dict[str, str] = {"period": period}
        if date_min:
            params["date_min"] = date_min
        if date_max:
            params["date_max"] = date_max
            
        return self.api_object.get_all(
            "reports/top_sellers",
            TopSellersReport,
            **params
        )
        
    # Settings
    def get_settings(self, group: str | None = None) -> list[SettingOption]:
        """
        Gets all settings or settings for a specific group.
        :param group: The settings group to get
        :return: list of SettingOption objects
        """
        endpoint = "settings"
        if group:
            endpoint = f"settings/{group}"
            
        return self.api_object.get_all(endpoint, SettingOption)
        
    def get_setting(self, group: str, id: str) -> SettingOption | None:
        """
        Gets a specific setting.
        :param group: The settings group
        :param id: The setting ID
        :return: SettingOption object or None if not found
        """
        return self.api_object.get(f"settings/{group}/{id}", SettingOption)
        
    def update_setting(
        self, group: str, id: str, setting: SettingOption
    ) -> SettingOption:
        """
        Updates a specific setting.
        :param group: The settings group
        :param id: The setting ID
        :param setting: SettingOption object with updates
        :return: updated SettingOption object
        """
        return self.api_object.put(f"settings/{group}/{id}", setting)
