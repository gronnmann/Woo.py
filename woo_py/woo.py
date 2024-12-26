from requests import Response
from woocommerce import API

from woo_py.models.webhook import Webhook


def _check_for_errors(response: Response) -> None:
    """
    Checks the response for errors and raises an exception if any are found.
    """
    response.raise_for_status()


class Woo:
    """
    Represents the main interface for accessing the API.
    """

    api_object: API  # official API object which will be used to make requests

    def __init__(self, api_object: API) -> None:
        self.api_object = api_object

    def create_webhook(self, webhook: Webhook) -> Webhook:
        """
        Creates a webhook.
        :param webhook: Webhook object
        :return: the created webhook
        """
        response = self.api_object.post("webhooks", webhook.dict())
        _check_for_errors(response)
        return Webhook.model_validate(response.json())

    def get_webhook(self, webhook_id: int) -> Webhook:
        """
        Gets a webhook by its ID.
        :param webhook_id: id of the webhook
        :return:
        """
        response = self.api_object.get(f"webhooks/{webhook_id}")
        _check_for_errors(response)
        return Webhook.model_validate(response.json())

    def delete_webhook(self, webhook_id: int, force: bool = False) -> None:
        """
        Deletes a webhook by its ID.
        :param webhook_id: id of the webhook
        :param force: when True, the webhook will be permanently deleted
        :return: None
        """
        response = self.api_object.delete(
            f"webhooks/{webhook_id}", params={"force": force}
        )
        _check_for_errors(response)

    def list_webhooks(self) -> list[Webhook]:
        """
        Lists all webhooks.
        :return: list of Webhook objects
        """
        response = self.api_object.get("webhooks")
        _check_for_errors(response)
        return [Webhook.model_validate(webhook) for webhook in response.json()]

    def update_webhook(self, webhook_id: int, webhook: Webhook) -> Webhook:
        """
        Updates a webhook by its ID.
        :param webhook_id: id of the webhook
        :param webhook: updated Webhook object
        :return:
        """
        response = self.api_object.put(f"webhooks/{webhook_id}", webhook.dict())
        _check_for_errors(response)
        return Webhook.model_validate(response.json())