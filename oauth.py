"""Implements one-legged OAuth 1.0 authentication for WooCommerce API requests.
Used for HTTP requests to the WooCommerce REST API.
"""

import time
import hashlib
import hmac
import base64
from typing import Literal
from urllib.parse import quote, urlencode, urljoin
import random
import string


class OAuth:
    """
    Class to handle one-legged OAuth 1.0a authentication.
    """

    def __init__(self, consumer_key: str, consumer_secret: str):
        """
        Initialize the OAuth class.

        :param consumer_key: The consumer key provided by WooCommerce.
        :param consumer_secret: The consumer secret provided by WooCommerce.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    @staticmethod
    def _percent_encode(value: str) -> str:
        """Percent-encode a string as per OAuth 1.0a specifications."""
        return quote(value, safe="/")

    def _generate_nonce(self, length: int = 32) -> str:
        """Generate a random nonce for the request."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _generate_signature(
        self, method: Literal["get", "post", "delete", "put"], url: str, params: dict[str, str]
    ) -> str:
        """
        Generate the OAuth signature.

        :param method: The HTTP method (e.g., GET, POST).
        :param url: The request URL.
        :param params: The parameters to include in the signature.
        :return: The generated signature.
        """
        # 1. Percent encode all keys and values
        encoded_params = {self._percent_encode(k): self._percent_encode(v) for k, v in params.items()}
        # 2. Sort the parameters by key
        sorted_params = dict(sorted(encoded_params.items()))
        # 3. Create the parameter string
        param_string = urlencode(sorted_params, safe="/")

        # 4. Create the signature base string
        base_string = "&".join([
            method.upper(),
            self._percent_encode(url),
            self._percent_encode(param_string)
        ])

        # 5. Create the signing key
        signing_key = f"{self._percent_encode(self.consumer_secret)}&"

        # 6. Generate the HMAC-SHA1 hash
        hashed = hmac.new(
            signing_key.encode(),
            base_string.encode(),
            hashlib.sha1
        )
        # 7. Return the base64 encoded signature
        return base64.b64encode(hashed.digest()).decode()

    def get_auth_params(self, method: str, url: str, additional_params: dict[str, str] = None) -> dict[str, str]:
        """
        Get OAuth parameters including the generated signature.

        :param method: The HTTP method (e.g., GET, POST).
        :param url: The request URL.
        :param additional_params: Any additional parameters to include in the request.
        :return: The complete set of OAuth parameters.
        """
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()

        # Base OAuth parameters
        params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": timestamp,
            "oauth_nonce": nonce,
        }

        if additional_params:
            params.update(additional_params)

        # Generate the OAuth signature
        signature = self._generate_signature(method, url, params)

        # Add the signature to the parameters
        params["oauth_signature"] = signature

        return params
