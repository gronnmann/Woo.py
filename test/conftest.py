import os
import random

import pytest
from dotenv import load_dotenv

from woo_py.api import API
from woo_py.woo import Woo


@pytest.fixture(scope="session")
def woo() -> Woo:
    load_dotenv()

    URL = os.getenv("WOO_URL")
    CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")
    VERIFY_SSL = os.getenv("VERIFY_SSL", "True").lower() == "true"

    if not URL or not CONSUMER_KEY or not CONSUMER_SECRET:
        raise ValueError("Missing WooCommerce credentials in .env file")

    api = API(
        URL,
        CONSUMER_KEY,
        CONSUMER_SECRET,
        verify_ssl=VERIFY_SSL,
    )

    try:
        response = api.get_json("/")
    except Exception as e:
        raise ValueError(f"Failed to connect to WooCommerce API: {e}")

    return Woo(api)


@pytest.fixture(scope="session")
def random_str() -> str:
    return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(4)])