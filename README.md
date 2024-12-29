# Woo.py
A wrapper around the official [python WooCommerce library](https://github.com/woocommerce/wc-api-python).

Simplifies the process of making requests to the WooCommerce API by providing a more practical interface,
using the official library together with pydantic models.

Note that this is very WIP and barely and endpoints are implemented.
They are mostly added as I need them in other projects.
You are welcome to contribute by adding more endpoints and models.
## Installation
Clone the repo, then do:
```bash
pip install ./Woo.py
```
You can now import the package and use it in your code.

## Known issues
- The `list_XXX` methods give `401 Unauthorized` errors when trying to list resources. 

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
# Running tests
To run the tests, you need to have a WooCommerce store running, and set the following environment variables
in `test/.env`:
- `WC_URL` - The URL to your WooCommerce store
- `WC_CONSUMER_KEY` - The consumer key for the WooCommerce API
- `WC_CONSUMER_SECRET` - The consumer secret for the WooCommerce API

After that, you can run the tests using `pytest`:
```bash
pytest test
```