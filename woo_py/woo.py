import datetime

from loguru import logger
from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin
from requests import Response, HTTPError
from woocommerce import API

from woo_py.models.coupon import Coupon
from woo_py.models.customer import Customer
from woo_py.models.webhook import Webhook
import typing as t

ContextType = t.Literal["view", "edit"]
OrderType = t.Literal["asc", "desc"]


def _check_for_errors(response: Response) -> None:
    """
    Checks the response for errors and raises an exception if any are found.
    """
    try:
        response.raise_for_status()
    except HTTPError as e:
        logger.error(f"Failed to make request: {e.response.content}")
        logger.error(f"Request content: {e.request.body}")
        raise


class Woo:
    """
    Represents the main interface for accessing the API.
    """

    api_object: API  # official API object which will be used to make requests

    def __init__(self, api_object: API) -> None:
        self.api_object = api_object

    def _get(
        self, endpoint: str, base_class: t.Type[BaseModel], **params
    ) -> BaseModel | None:
        """
        Gets an object from an endpoint.
        :return parsed object or None if not found
        """
        logger.debug(f"Getting {endpoint} with params {params}")
        response = self.api_object.get(endpoint, params=params)
        if response.status_code == 404:
            return None
        _check_for_errors(response)
        return base_class.model_validate(response.json())

    def _get_all(
        self, endpoint: str, base_class: t.Type[BaseModel], **params
    ) -> list[t.Any]:
        """
        Gets all objects from an endpoint.
        """

        # delete all None params
        params = {k: v for k, v in params.items() if v is not None}

        logger.debug(f"Getting all {endpoint} with params {params}")

        response = self.api_object.get(endpoint, params=params)
        _check_for_errors(response)
        return [base_class.model_validate(obj) for obj in response.json()]

    def _post(
        self, endpoint: str, model: [BaseModel, ChangeDetectionMixin]
    ) -> BaseModel:
        """
        Posts an object to an endpoint.

        :param endpoint: the endpoint to post to
        :param model: the model to post

        :return: the created object
        """

        base_class = type(model)

        dumped = model.model_dump(exclude_none=True)

        logger.debug(f"Posting to {endpoint} with model {dumped}")

        response = self.api_object.post(endpoint, data=None, json=dumped)
        _check_for_errors(response)
        return base_class.model_validate(response.json())

    def _put(self, endpoint: str, model: [BaseModel, ChangeDetectionMixin]) -> t.Any:
        """
        Puts an object to an endpoint.

        :param endpoint: the endpoint to put to
        :param model: the model to put

        :return: the updated object
        """

        base_class = type(model)

        logger.debug(
            f"Putting to {endpoint} with model {model.model_dump(exclude_unchanged=True)}"
        )

        response = self.api_object.put(
            endpoint, data=None, json=model.model_dump(exclude_unchanged=True)
        )
        _check_for_errors(response)
        return base_class.model_validate(response.json())

    def _delete(self, endpoint: str, **params) -> None:
        """
        Deletes an object from an endpoint.
        """

        response = self.api_object.delete(endpoint, params=params)
        _check_for_errors(response)

    # Coupons
    def create_coupon(self, coupon: Coupon):
        """
        Creates a coupon.
        :param coupon: Coupon object
        :return: the created coupon
        """
        response = self.api_object.post("coupons", data=coupon.model_dump_json())
        _check_for_errors(response)
        return Coupon.model_validate(response.json())

    def get_coupon(self, coupon_id: int) -> Coupon | None:
        """
        Gets a coupon by its ID.
        :param coupon_id: id of the coupon
        :return:
        """
        return self._get(f"coupons/{coupon_id}", Coupon)

    def list_coupons(
        self,
        context: ContextType = "view",
        page: int = 0,
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

        return self._get_all(
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
        return self._put(f"coupons/{coupon_id}", coupon)

    def delete_coupon(self, coupon_id: int) -> None:
        """
        Deletes a coupon by its ID.
        :param coupon_id: id of the coupon
        :return: None
        """
        self._delete(f"coupons/{coupon_id}")

    # Webhooks

    def create_webhook(self, webhook: Webhook) -> Webhook:
        """
        Creates a webhook.
        :param webhook: Webhook object
        :return: the created webhook
        """
        return self._post("webhooks", webhook)

    def get_webhook(self, webhook_id: int) -> Webhook | None:
        """
        Gets a webhook by its ID.
        :param webhook_id: id of the webhook
        :return:
        """
        return self._get(f"webhooks/{webhook_id}", Webhook)

    def delete_webhook(self, webhook_id: int, force: bool = False) -> None:
        """
        Deletes a webhook by its ID.
        :param webhook_id: id of the webhook
        :param force: when True, the webhook will be permanently deleted
        :return: None
        """
        return self._delete(f"webhooks/{webhook_id}", force=force)

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
        return self._get_all(
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
        return self._put(f"webhooks/{webhook_id}", webhook)

    # Customers

    def create_customer(self, customer: Customer) -> BaseModel:
        """
        Creates a customer.
        :param customer: Customer object
        :return: the created customer
        """
        return self._post("customers", customer)

    def get_customer(self, customer_id: int) -> BaseModel | None:
        """
        Gets a customer by its ID.
        :param customer_id: id of the customer
        :return:
        """
        return self._get(f"customers/{customer_id}", Customer)

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

        return self._get_all(
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
        return self._put(f"customers/{customer_id}", customer)

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

        self._delete(f"customers/{customer_id}")
