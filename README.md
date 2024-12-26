# Woo.py
A wrapper around the official [python WooCommerce library](https://github.com/woocommerce/wc-api-python).

Simplifies the process of making requests to the WooCommerce API by providing a more practical interface,
using the official library together with pydantic models.

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
woo_py = Woo(api)
```
You can then use the `woo_py` object to make requests to the WooCommerce API.
For example, for POSTing webhooks:
```python
woo_py.create_webhook(webhook={your webhook here})
```
Take a look at the `woo.py` file to see all the available methods, and in the `models` folder for 
the defined models. 
These correspond to the ones found [here](https://woocommerce.github.io/woocommerce-rest-api-docs/)