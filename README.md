# Woo.py
A wrapper around the official [python WooCommerce library](https://github.com/woocommerce/wc-api-python).

Simplifies the process of making requests to the WooCommerce API by providing a more practical interface,
using the official library together with pydantic models.

Note that this is a work in progress, which I mostly update when I use the endpoints in my own projects.
You are therefore not guaranteed that all endpoints are implemented, but I will try to keep it up to date.

## Installation
Clone the repo, then do:
```bash
pip install ./Woo.py
```
You can now import the package and use it in your code.

## Usage
After installation, create an instance of the `API` object from the `WooCommerce` library.
After that, you can use the wrapper in the following way:
```python


wcapi = API(
    url="http://example.com",
    consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    version="wc/v3"
)

woo_py = Woo(wcapi)
```
You can then use the `woo_py` object to make requests to the WooCommerce API.
For example, for POSTing webhooks:
```python
from woocommerce import API
from woo_py.woo import Woo


webhook = Webhook(
    name="My webhook",
    topic=WebhookTopic.ORDER_CREATED,
    delivery_url="https://example.com/webhook",
    status="active"
)
woo_py.create_webhook(webhook)
```
Take a look at the `woo.py` file to see all the available methods, and in the `models` folder for 
the defined models. 
These correspond to the ones found [here](https://woocommerce.github.io/woocommerce-rest-api-docs/)