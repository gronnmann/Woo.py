from pydantic import BaseModel

from woo_py.models.coupon import Coupon
from woo_py.models.customer import Customer
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
