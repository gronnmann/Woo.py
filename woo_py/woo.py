import typing as t
from pydantic import BaseModel

from woo_py.models import Order
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
from woo_py.models.order_refund import OrderRefund

from woo_py.api import API, PaginatedResponse

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
    
    @t.overload
    def list_coupons(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "modified", "id", "include", "title", "slug"
            ] = None,
            code: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[Coupon]: ...
    
    @t.overload
    def list_coupons(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "modified", "id", "include", "title", "slug"
            ] = None,
            code: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[Coupon]: ...
    
    @t.overload
    def list_coupons(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "modified", "id", "include", "title", "slug"
            ] = None,
            code: str | None = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[Coupon]: ...
    
    def list_coupons(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "modified", "id", "include", "title", "slug"
            ] = None,
            code: str | None = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[Coupon] | PaginatedResponse[Coupon]:
        """
        Lists all coupons.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of Coupon objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
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
            "code": code,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        return self.api_object.get_all(
            "coupons",
            Coupon,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_webhooks(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "title"] = None,
            status: t.Literal["all", "active", "paused", "disabled", "all"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[Webhook]: ...
    
    @t.overload
    def list_webhooks(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "title"] = None,
            status: t.Literal["all", "active", "paused", "disabled", "all"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[Webhook]: ...
    
    @t.overload
    def list_webhooks(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "title"] = None,
            status: t.Literal["all", "active", "paused", "disabled", "all"] = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[Webhook]: ...
    
    def list_webhooks(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "title"] = None,
            status: t.Literal["all", "active", "paused", "disabled", "all"] = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[Webhook] | PaginatedResponse[Webhook]:
        """
        Lists all webhooks.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of Webhook objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
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
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            "webhooks/",
            Webhook,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_customers(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "registered_date"] = None,
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
            ] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[Customer]: ...
    
    @t.overload
    def list_customers(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "registered_date"] = None,
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
            ] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[Customer]: ...
    
    @t.overload
    def list_customers(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "registered_date"] = None,
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
            ] = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[Customer]: ...
    
    def list_customers(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "registered_date"] = None,
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
            ] = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[Customer] | PaginatedResponse[Customer]:
        """
        Lists all customers
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of Customer objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        params = {
            "context": context,
            "page": page,
            "per_page": per_page,
            "search": search,
            "exclude": exclude,
            "include": include,
            "offset": offset,
            "order": order,
            "orderby": orderby,
            "email": email,
            "role": role,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        return self.api_object.get_all(
            "customers",
            Customer,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_tax_classes(
        self,
        *,
        follow_pages: t.Literal[False] = False,
        return_metadata: t.Literal[True],
    ) -> PaginatedResponse[TaxClass]: ...
    
    @t.overload
    def list_tax_classes(
        self,
        *,
        follow_pages: t.Literal[False] = False,
        return_metadata: t.Literal[False] = False,
    ) -> list[TaxClass]: ...
    
    @t.overload
    def list_tax_classes(
        self,
        *,
        follow_pages: t.Literal[True],
        return_metadata: t.Literal[False] = False,
    ) -> list[TaxClass]: ...
    
    def list_tax_classes(
        self,
        follow_pages: bool = False,
        return_metadata: bool = False,
    ) -> list[TaxClass] | PaginatedResponse[TaxClass]:
        """
        Lists all tax classes.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of TaxClass objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        return self.api_object.get_all(
            "taxes/classes", 
            TaxClass, 
            follow_pages=follow_pages,
            include_metadata=return_metadata
        )

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
    
    @t.overload
    def list_products(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "id", "include", "title", "slug", "price", "popularity", "rating"
            ] = None,
            category: str | None = None,
            tag: str | None = None,
            status: t.Literal["any", "draft", "pending", "private", "publish"] = None,
            type: t.Literal["simple", "grouped", "external", "variable"] = None,
            featured: bool | None = None,
            sku: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[Product]: ...
    
    @t.overload
    def list_products(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "id", "include", "title", "slug", "price", "popularity", "rating"
            ] = None,
            category: str | None = None,
            tag: str | None = None,
            status: t.Literal["any", "draft", "pending", "private", "publish"] = None,
            type: t.Literal["simple", "grouped", "external", "variable"] = None,
            featured: bool | None = None,
            sku: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[Product]: ...
    
    @t.overload
    def list_products(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "id", "include", "title", "slug", "price", "popularity", "rating"
            ] = None,
            category: str | None = None,
            tag: str | None = None,
            status: t.Literal["any", "draft", "pending", "private", "publish"] = None,
            type: t.Literal["simple", "grouped", "external", "variable"] = None,
            featured: bool | None = None,
            sku: str | None = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[Product]: ...
    
    def list_products(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal[
                "date", "id", "include", "title", "slug", "price", "popularity", "rating"
            ] = None,
            category: str | None = None,
            tag: str | None = None,
            status: t.Literal["any", "draft", "pending", "private", "publish"] = None,
            type: t.Literal["simple", "grouped", "external", "variable"] = None,
            featured: bool | None = None,
            sku: str | None = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[Product] | PaginatedResponse[Product]:
        """
        Lists all products.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of Product objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
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
            "category": category,
            "tag": tag,
            "status": status,
            "type": type,
            "featured": featured,
            "sku": sku,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        return self.api_object.get_all(
            "products",
            Product,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_product_variations(
            self,
            product_id: int,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "include", "title", "slug"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[ProductVariation]: ...
    
    @t.overload
    def list_product_variations(
            self,
            product_id: int,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "include", "title", "slug"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductVariation]: ...
    
    @t.overload
    def list_product_variations(
            self,
            product_id: int,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "include", "title", "slug"] = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductVariation]: ...
    
    def list_product_variations(
            self,
            product_id: int,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "id", "include", "title", "slug"] = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[ProductVariation] | PaginatedResponse[ProductVariation]:
        """
        Lists all variations for a product.
        
        :param product_id: id of the parent product
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of ProductVariation objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
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
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            f"products/{product_id}/variations",
            ProductVariation,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_product_categories(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            parent: int | None = None,
            product: int | None = None,
            slug: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[ProductCategory]: ...
    
    @t.overload
    def list_product_categories(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            parent: int | None = None,
            product: int | None = None,
            slug: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductCategory]: ...
    
    @t.overload
    def list_product_categories(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            parent: int | None = None,
            product: int | None = None,
            slug: str | None = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductCategory]: ...
    
    def list_product_categories(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            parent: int | None = None,
            product: int | None = None,
            slug: str | None = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[ProductCategory] | PaginatedResponse[ProductCategory]:
        """
        Lists all product categories.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of ProductCategory objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        params = {
            "context": context,
            "page": page,
            "per_page": per_page,
            "search": search,
            "exclude": exclude,
            "include": include,
            "order": order,
            "orderby": orderby,
            "hide_empty": hide_empty,
            "parent": parent,
            "product": product,
            "slug": slug,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            "products/categories",
            ProductCategory,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_product_tags(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            product: int | None = None,
            slug: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[ProductTag]: ...
    
    @t.overload
    def list_product_tags(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            product: int | None = None,
            slug: str | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductTag]: ...
    
    @t.overload
    def list_product_tags(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            product: int | None = None,
            slug: str | None = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductTag]: ...
    
    def list_product_tags(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["id", "include", "name", "slug", "term_group", "description", "count"] = None,
            hide_empty: bool = None,
            product: int | None = None,
            slug: str | None = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[ProductTag] | PaginatedResponse[ProductTag]:
        """
        Lists all product tags.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of ProductTag objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        params = {
            "context": context,
            "page": page,
            "per_page": per_page,
            "search": search,
            "exclude": exclude,
            "include": include,
            "offset": offset,
            "order": order,
            "orderby": orderby,
            "hide_empty": hide_empty,
            "product": product,
            "slug": slug,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            "products/tags",
            ProductTag,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_product_attributes(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            order: OrderType = None,
            orderby: t.Literal["id", "name", "slug", "type", "order_by"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[ProductAttribute]: ...
    
    @t.overload
    def list_product_attributes(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            order: OrderType = None,
            orderby: t.Literal["id", "name", "slug", "type", "order_by"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductAttribute]: ...
    
    @t.overload
    def list_product_attributes(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            order: OrderType = None,
            orderby: t.Literal["id", "name", "slug", "type", "order_by"] = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductAttribute]: ...
    
    def list_product_attributes(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            order: OrderType = None,
            orderby: t.Literal["id", "name", "slug", "type", "order_by"] = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[ProductAttribute] | PaginatedResponse[ProductAttribute]:
        """
        Lists all product attributes.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of ProductAttribute objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        params = {
            "context": context,
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            "products/attributes",
            ProductAttribute,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    
    @t.overload
    def list_product_reviews(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "date_gmt", "id", "include", "product", "rating"] = None,
            reviewer: str | None = None,
            reviewer_email: str | None = None,
            product: int | None = None,
            status: t.Literal["approved", "hold", "spam", "unspam", "trash", "untrash"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[ProductReview]: ...
    
    @t.overload
    def list_product_reviews(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "date_gmt", "id", "include", "product", "rating"] = None,
            reviewer: str | None = None,
            reviewer_email: str | None = None,
            product: int | None = None,
            status: t.Literal["approved", "hold", "spam", "unspam", "trash", "untrash"] = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductReview]: ...
    
    @t.overload
    def list_product_reviews(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "date_gmt", "id", "include", "product", "rating"] = None,
            reviewer: str | None = None,
            reviewer_email: str | None = None,
            product: int | None = None,
            status: t.Literal["approved", "hold", "spam", "unspam", "trash", "untrash"] = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[ProductReview]: ...
    
    def list_product_reviews(
            self,
            context: ContextType = None,
            page: int = None,
            per_page: int = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType = None,
            orderby: t.Literal["date", "date_gmt", "id", "include", "product", "rating"] = None,
            reviewer: str | None = None,
            reviewer_email: str | None = None,
            product: int | None = None,
            status: t.Literal["approved", "hold", "spam", "unspam", "trash", "untrash"] = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[ProductReview] | PaginatedResponse[ProductReview]:
        """
        Lists all product reviews.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of ProductReview objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
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
            "reviewer": reviewer,
            "reviewer_email": reviewer_email,
            "product": product,
            "status": status,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            "products/reviews",
            ProductReview,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
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
    @t.overload
    def list_payment_gateways(
        self,
        *,
        follow_pages: t.Literal[False] = False,
        return_metadata: t.Literal[True],
    ) -> PaginatedResponse[PaymentGateway]: ...
    
    @t.overload
    def list_payment_gateways(
        self,
        *,
        follow_pages: t.Literal[False] = False,
        return_metadata: t.Literal[False] = False,
    ) -> list[PaymentGateway]: ...
    
    @t.overload
    def list_payment_gateways(
        self,
        *,
        follow_pages: t.Literal[True],
        return_metadata: t.Literal[False] = False,
    ) -> list[PaymentGateway]: ...
    
    def list_payment_gateways(
        self,
        follow_pages: bool = False,
        return_metadata: bool = False,
    ) -> list[PaymentGateway] | PaginatedResponse[PaymentGateway]:
        """
        Lists all payment gateways.
        
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of PaymentGateway objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        return self.api_object.get_all(
            "payment_gateways",
            PaymentGateway,
            follow_pages=follow_pages,
            include_metadata=return_metadata,
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
    def get_countries(self, follow_pages: bool = False) -> list[Country]:
        """
        Gets all countries.
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :return: list of Country objects
        """
        return self.api_object.get_all("data/countries", Country, follow_pages=follow_pages)

    def get_country(self, country_code: str) -> Country | None:
        """
        Gets a country by its code.
        :param country_code: two-character country code
        :return: Country object or None if not found
        """
        return self.api_object.get(f"data/countries/{country_code}", Country)

    def get_currencies(self, follow_pages: bool = False) -> list[Currency]:
        """
        Gets all currencies.
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :return: list of Currency objects
        """
        return self.api_object.get_all("data/currencies", Currency, follow_pages=follow_pages)

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
            
        sales_report = self.api_object.get_all("reports/sales", SalesReport, **params)

        if sales_report:
            return sales_report[0]
        return None

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

    # Order Refunds
    def create_order_refund(self, order_id: int, refund: OrderRefund) -> OrderRefund:
        """
        Creates a refund for a given order.
        :param order_id: id of the order
        :param refund: OrderRefund object with refund data
        :return: the created OrderRefund object
        """
        return self.api_object.post(f"orders/{order_id}/refunds", refund)

    def get_order_refund(self, order_id: int, refund_id: int) -> OrderRefund | None:
        """
        Retrieves a refund for a given order by its refund ID.
        :param order_id: id of the order
        :param refund_id: id of the refund
        :return: OrderRefund object or None if not found
        """
        return self.api_object.get(f"orders/{order_id}/refunds/{refund_id}", OrderRefund)
    
    
    @t.overload
    def list_order_refunds(
            self,
            order_id: int,
            context: str = None,
            page: int = None,
            per_page: int = None,
            search: str = None,
            after: str = None,
            before: str = None,
            exclude: list[int] = None,
            include: list[int] = None,
            offset: int = None,
            order: str = None,
            orderby: str = None,
            dp: int = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[OrderRefund]: ...
    
    @t.overload
    def list_order_refunds(
            self,
            order_id: int,
            context: str = None,
            page: int = None,
            per_page: int = None,
            search: str = None,
            after: str = None,
            before: str = None,
            exclude: list[int] = None,
            include: list[int] = None,
            offset: int = None,
            order: str = None,
            orderby: str = None,
            dp: int = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[OrderRefund]: ...
    
    @t.overload
    def list_order_refunds(
            self,
            order_id: int,
            context: str = None,
            page: int = None,
            per_page: int = None,
            search: str = None,
            after: str = None,
            before: str = None,
            exclude: list[int] = None,
            include: list[int] = None,
            offset: int = None,
            order: str = None,
            orderby: str = None,
            dp: int = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[OrderRefund]: ...
    
    def list_order_refunds(
            self,
            order_id: int,
            context: str = None,
            page: int = None,
            per_page: int = None,
            search: str = None,
            after: str = None,
            before: str = None,
            exclude: list[int] = None,
            include: list[int] = None,
            offset: int = None,
            order: str = None,
            orderby: str = None,
            dp: int = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[OrderRefund] | PaginatedResponse[OrderRefund]:
        """
        Lists all refunds for a given order.
        
        :param order_id: id of the order
        :param context: scope under which the request is made; determines fields present in the response
        :param page: current page of the collection
        :param per_page: maximum number of items returned per page
        :param search: limit results to those matching a string
        :param after: limit response to resources published after a given ISO8601-compliant date
        :param before: limit response to resources published before a given ISO8601-compliant date
        :param exclude: list of refund IDs to exclude from results
        :param include: list of refund IDs to include in results
        :param offset: offset the result set by a specific number of items
        :param order: sort attribute order (asc or desc)
        :param orderby: attribute by which to sort the collection
        :param dp: number of decimal points to use for each resource
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of OrderRefund objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
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
            "dp": dp,
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        return self.api_object.get_all(
            f"orders/{order_id}/refunds", 
            OrderRefund, 
            follow_pages=follow_pages, 
            include_metadata=return_metadata,
            **params
        )

    def delete_order_refund(self, order_id: int, refund_id: int, force: bool = None) -> None:
        """
        Deletes an order refund by its ID.
        :param order_id: id of the order
        :param refund_id: id of the refund
        :param force: if True, the refund will be permanently deleted
        :return: None
        """
        self.api_object.delete(f"orders/{order_id}/refunds/{refund_id}", force=force)

    def create_order(self, order: Order) -> Order:
        """
        Creates an order.
        :param order: Order object containing order details.
        :return: The created Order object.
        """
        return self.api_object.post("orders", order)

    def get_order(self, order_id: int) -> Order | None:
        """
        Retrieves an order by its ID.
        :param order_id: The ID of the order.
        :return: The Order object if found, otherwise None.
        """
        return self.api_object.get(f"orders/{order_id}", Order)
    
    @t.overload
    def list_orders(
            self,
            context: ContextType | None = None,
            page: int | None = None,
            per_page: int | None = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            modified_after: str | None = None,
            modified_before: str | None = None,
            dates_are_gmt: bool | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType | None = None,
            orderby: t.Literal["date", "modified", "id", "include", "title", "slug"] | None = None,
            parent: list[int] | None = None,
            parent_exclude: list[int] | None = None,
            status: list[str] | None = None,
            customer: int | None = None,
            product: int | None = None,
            dp: int | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[True],
    ) -> PaginatedResponse[Order]: ...
    
    @t.overload
    def list_orders(
            self,
            context: ContextType | None = None,
            page: int | None = None,
            per_page: int | None = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            modified_after: str | None = None,
            modified_before: str | None = None,
            dates_are_gmt: bool | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType | None = None,
            orderby: t.Literal["date", "modified", "id", "include", "title", "slug"] | None = None,
            parent: list[int] | None = None,
            parent_exclude: list[int] | None = None,
            status: list[str] | None = None,
            customer: int | None = None,
            product: int | None = None,
            dp: int | None = None,
            *,
            follow_pages: t.Literal[False] = False,
            return_metadata: t.Literal[False] = False,
    ) -> list[Order]: ...
    
    @t.overload
    def list_orders(
            self,
            context: ContextType | None = None,
            page: int | None = None,
            per_page: int | None = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            modified_after: str | None = None,
            modified_before: str | None = None,
            dates_are_gmt: bool | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType | None = None,
            orderby: t.Literal["date", "modified", "id", "include", "title", "slug"] | None = None,
            parent: list[int] | None = None,
            parent_exclude: list[int] | None = None,
            status: list[str] | None = None,
            customer: int | None = None,
            product: int | None = None,
            dp: int | None = None,
            *,
            follow_pages: t.Literal[True],
            return_metadata: t.Literal[False] = False,
    ) -> list[Order]: ...
    
    def list_orders(
            self,
            context: ContextType | None = None,
            page: int | None = None,
            per_page: int | None = None,
            search: str | None = None,
            after: str | None = None,
            before: str | None = None,
            modified_after: str | None = None,
            modified_before: str | None = None,
            dates_are_gmt: bool | None = None,
            exclude: list[int] | None = None,
            include: list[int] | None = None,
            offset: int | None = None,
            order: OrderType | None = None,
            orderby: t.Literal["date", "modified", "id", "include", "title", "slug"] | None = None,
            parent: list[int] | None = None,
            parent_exclude: list[int] | None = None,
            status: list[str] | None = None,
            customer: int | None = None,
            product: int | None = None,
            dp: int | None = None,
            follow_pages: bool = False,
            return_metadata: bool = False,
    ) -> list[Order] | PaginatedResponse[Order]:
        """
        Lists orders with optional filtering.
        Available parameters include:
          - context: Scope under which the request is made (e.g. "view" or "edit").
          - page: Current page of the collection.
          - per_page: Maximum number of orders per page.
          - search: Limit results to those matching a string.
          - after / before: Limit results to orders created within a date range.
          - modified_after / modified_before: Filter orders by modification dates.
          - dates_are_gmt: Whether the dates are in GMT.
          - exclude / include: Lists of order IDs to exclude/include.
          - offset: Offset for the result set.
          - order: Sorting order ("asc" or "desc").
          - orderby: Attribute by which to sort orders.
          - parent / parent_exclude: Filter by parent order IDs.
          - status: Filter by order statuses.
          - customer: Filter orders for a specific customer ID.
          - product: Filter orders that contain a specific product ID.
          - dp: Number of decimal points to include.
          - follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
          - return_metadata: If True, returns a PaginatedResponse with metadata instead of just a list. Cannot be used with follow_pages=True.
        :return: A list of Order objects or a PaginatedResponse containing the list and pagination metadata.
        """
        if follow_pages and return_metadata:
            raise ValueError("Cannot use follow_pages=True with return_metadata=True")
            
        params = {
            "context": context,
            "page": page,
            "per_page": per_page,
            "search": search,
            "after": after,
            "before": before,
            "modified_after": modified_after,
            "modified_before": modified_before,
            "dates_are_gmt": dates_are_gmt,
            "exclude": exclude,
            "include": include,
            "offset": offset,
            "order": order,
            "orderby": orderby,
            "parent": parent,
            "parent_exclude": parent_exclude,
            "status": status,
            "customer": customer,
            "product": product,
            "dp": dp,
        }
        # Remove any parameters that are None.
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.api_object.get_all(
            "orders", 
            Order, 
            follow_pages=follow_pages,
            include_metadata=return_metadata,
            **params
        )

    def update_order(self, order_id: int, order: Order) -> Order:
        """
        Updates an order by its ID.
        :param order_id: The ID of the order to update.
        :param order: Order object containing updated data.
        :return: The updated Order object.
        """
        return self.api_object.put(f"orders/{order_id}", order)

    def delete_order(self, order_id: int, force: bool = False) -> None:
        """
        Deletes an order by its ID.
        :param order_id: The ID of the order.
        :param force: If True, the order will be permanently deleted.
        :return: None.
        """
        self.api_object.delete(f"orders/{order_id}", force=force)
