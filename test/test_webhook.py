from woo_py.models.webhook import Webhook
from woo_py.woo import Woo


def test_all_methods(woo: Woo):
    new_webhook = Webhook(
        name="test_webhook",
        topic="customer.created",
        delivery_url="http://localhost/test"
    )

    created_webhook = woo.create_webhook(new_webhook)
    assert created_webhook.id is not None

    found_webhook = woo.get_webhook(created_webhook.id)
    assert found_webhook is not None
    assert found_webhook.id == created_webhook.id

    found_webhook.name = "test_webhook_updated"
    updated_webhook = woo.update_webhook(found_webhook.id, found_webhook)
    assert updated_webhook.id == found_webhook.id

    all_webhooks = woo.list_webhooks(include=[updated_webhook.id])
    assert len(all_webhooks) > 0
    assert updated_webhook.id in [wh.id for wh in all_webhooks]

    woo.delete_webhook(updated_webhook.id)
    assert woo.get_webhook(updated_webhook.id) is None