# Woo.py
An unofficial wrapper around the official [WooCommerce REST API](https://woocommerce.github.io/woocommerce-rest-api-docs/).

Simplifies the process of making requests to the WooCommerce API by providing a more practical interface,
using pydantic models together with the httpx library for more efficient resource access.

Has several advantages over the official library:
- Uses pydantic models to validate the data before sending it to the API, and to parse the response.
- Provides a more practical interface for making requests to the API.

Note that this is very WIP and barely and endpoints are implemented.
They are mostly added as I need them in other projects.
You are welcome to contribute by adding more endpoints and models.

Currently, HTTP requests are not implemented yet. 
You can however run it on self-signed certificated by setting the `verify_ssl` parameter of the `API` object to `False`.

If you wish to run Woo on `localhost` with HTTPS, I recommend my [docker setup](https://github.com/gronnmann/wordpress_localhost_https). 

## Installation
Clone the repo, then do:
```bash
pip install ./Woo.py
```
You can now import the package and use it in your code.

## Usage
After installation, create an instance of the `API` object. For details on parameters,
see the `api.py` file (its all type hinted :) ).  
After that, you can use the wrapper in the following way:
```python
from woo_py.api import API
from woo_py.woo import Woo

wcapi = API(
    url="http://example.com",
    consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
)

woo_py = Woo(wcapi)
```
You can then use the `woo_py` object to make requests to the WooCommerce API.
For example, for POSTing webhooks:
```python
from woo_py.models.webhook import Webhook, WebhookTopic

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

### Paginated responses
All `list_xxx` methods often contain paginated content. By default, the API will return the first page.
You can use `follow_pages=True` to get all pages.

This will return a list of all items in the response.

If you for some reason need the pagination metadata, you can use `return_metadata=True`.

In that case, the response will be a `PaginatedResponse[type]`, where the objects are available under
`paginated_response.items`, and the metadata is available in the model.

Examples:
```python
# Get all orders in first page
orders = woo.list_orders() # type: list[Order]

# Get all orders in all pages
orders = woo.list_orders(follow_pages=True) # type: list[Order] 

# Get all orders in first page, including paging metadata
orders_page_metadata = woo.list_orders(return_metadata=True) # type: PaginatedResponse[Order]
orders = orders_page_metadata.items # type: list[Order]

```


# Running tests
To run the tests, you need to have a WooCommerce store running, and set the following environment variables
in `test/.env`:
- `WC_URL` - The URL to your WooCommerce store
- `WC_CONSUMER_KEY` - The consumer key for the WooCommerce API
- `WC_CONSUMER_SECRET` - The consumer secret for the WooCommerce API
- `VERIFY_SSL` - Whenever to verify the SSL certificate of the WooCommerce store. Set to `False` if you are using a self-signed certificate.

After that, you can run the tests using `pytest`:
```bash
pytest test
```