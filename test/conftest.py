import os

import pytest
from dotenv import load_dotenv
from woocommerce import API

from woo_py.woo import Woo


@pytest.fixture(scope="session")
def woo() -> Woo:
    load_dotenv()

    URL = os.getenv("WOO_URL")
    CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")

    if not URL or not CONSUMER_KEY or not CONSUMER_SECRET:
        raise ValueError("Missing WooCommerce credentials in .env file")

    api = API(
        URL,
        CONSUMER_KEY,
        CONSUMER_SECRET,
    )

    response = api.get("/")
    try:
        response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Failed to connect to WooCommerce API: {e}")

    return Woo(api)