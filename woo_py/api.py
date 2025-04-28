"""
Package for handling requests to the WOO API.
"""

import json
from urllib.parse import urljoin, urlparse

import httpx
from httpx import BasicAuth
from loguru import logger
import typing as t

from pydantic import BaseModel
from pydantic_changedetect import ChangeDetectionMixin


def _is_ssl(url: str) -> bool:
    """Check if url use HTTPS.

    :param: url: The URL to check.
    :return: Whenever the URL uses HTTPS.
    """

    parsed_url = urlparse(url)

    return parsed_url.scheme == "https"


T = t.TypeVar("T", bound=BaseModel)

URLParams = (
    str
    | float
    | int
    | bool
    | None
    | list[str | float | int | bool]
    | list[str]
    | list[int]
    | list[float]
    | list[bool]
)


def _parse_woo_error_json(response: httpx.Response) -> str:
    """
    Parse the error JSON from a WooCommerce response.

    :param response: The response.
    :return: The error message.
    """

    try:
        error_json = response.json()
    except json.JSONDecodeError:
        return f"Failed to parse error JSON: {response.text}"

    detail_str = ""

    data = error_json.get("data", {})
    detail_str += f"\nStatus: {data.get('status', 'Unknown status')}"

    if data.get("details"):
        details = data.get("details", {})
        detail_str += str(details)
        for detail in details.keys():
            detail_element = details.get(detail, {})

            detail_str += f"\n{detail_element.get('code', 'Unknown code')}: {detail_element.get('message', 'No message')}"

    msg = (
        f"{error_json.get('code', 'Unknown code')}: {error_json.get('message', 'No message')}\n"
        f"Details: {detail_str}"
    )

    return msg


class API:
    """
    Class for doing requests to the WooCommerce API.
    """

    _client: httpx.Client
    """The HTTPX client to use for requests."""

    _url: str
    """The URL of the WooCommerce API."""

    _consumer_key: str
    """The consumer key for the API."""

    _consumer_secret: str
    """The consumer secret for the API."""

    _is_ssl: bool
    """Check if url use HTTPS"""

    _verify_ssl: bool
    """Whenever to verify SSL certificate. Need to be set to False for self-signed certificates."""

    _query_string_auth: bool
    """Whenever to authenticate using url params (include consumer key and secret in URL). Requires HTTPS."""

    timeout: float = 10.0

    def __init__(
        self,
        url: str,
        consumer_key: str,
        consumer_secret: str,
        query_string_auth: bool = False,
        verify_ssl: bool = True,
        timeout: float = 10.0,
    ) -> None:
        """
        Initialize the API client.

        :param url: The URL of the WooCommerce API.
        :param consumer_key: The consumer key.
        :param consumer_secret: The consumer secret.
        :param verify_ssl: Whenever to verify SSL certificate. Need to be set to False for self-signed certificates.
        :param query_string_auth: Whenever to authenticate using url params (include consumer key and secret in URL).
        :param timeout: The timeout for requests.
        Requires HTTPS.
        """

        self._url = url
        self._query_string_auth = query_string_auth

        self._client = httpx.Client(
            headers={
                "User-Agent": "WooPy/0.0.2",
                "Accept": "application/json",
            },
            base_url=urljoin(self._url, "/wp-json/wc/v3/"),
            verify=verify_ssl,
            timeout=timeout,
        )

        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret

        self._is_ssl = _is_ssl(self._url)

        censored_secret = self._consumer_secret[-4:]
        logger.debug(
            f"Initializing API client for {self._url} with key {self._consumer_key} and secret "
            f":{censored_secret}."
        )

        if not self._is_ssl:
            logger.warning("The API URL is not using HTTPS. This is not recommended.")
        if not verify_ssl:
            logger.warning(
                "SSL certificate verification is disabled. This is not recommended."
            )

    def __del__(self) -> None:
        self._client.close()

    def _request(
        self,
        endpoint: str,
        method: t.Literal["post", "get", "put", "delete"],
        data: dict[str, t.Any] | BaseModel | ChangeDetectionMixin | None = None,
        **kwargs: URLParams,
    ) -> httpx.Response:
        """
        Do requests.
        For HTTPS, either basic or query string auth is used.
        For HTTP, 'one-legged' OAuth is used.
        For reference: https://woocommerce.github.io/woocommerce-rest-api-docs/#authentication

        :param method: The HTTP method to use.
        :param endpoint: The endpoint to request.
        :param data: The data to send.
        :param kwargs: Additional keyword arguments.
        :return: The response.
        """

        kwargs = kwargs or {}

        # Convert list parameters to comma-separated strings
        for key, value in list(kwargs.items()):
            if isinstance(value, list):
                kwargs[key] = ','.join(str(item) for item in value)

        # Delete None kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        auth: BasicAuth | None = None

        if self._is_ssl:
            """For SSL, both basic and query string auth is supported."""
            if self._query_string_auth:
                kwargs.update(
                    {
                        "consumer_key": self._consumer_key,
                        "consumer_secret": self._consumer_secret,
                    }
                )
            else:
                auth = BasicAuth(self._consumer_key, self._consumer_secret)
        else:
            """Without SSL, only OAUTH url is supported"""
            raise NotImplementedError("OAuth is not supported for non-HTTPS URLs.")

        sent_data: str | dict[str, t.Any] | None = None

        if issubclass(data.__class__, ChangeDetectionMixin) and method == "put":
            json_dumped = data.model_dump_json(exclude_unchanged=True, exclude_unset=True)  # type: ignore
            print(f"excluding unchanged")
            sent_data = json.loads(
                json_dumped
            )  # Stupid workaround as we can't send text directly,
            # but also sending the whole object gives 'datetime' is not JSON serializable
        elif issubclass(data.__class__, BaseModel):
            json_dumped = data.model_dump_json(exclude_unset=True)
            sent_data = json.loads(json_dumped)
        else:
            sent_data = data

        response = self._client.request(
            method,
            endpoint,
            json=sent_data,
            auth=auth,
            params=kwargs,
        )

        logger.debug(f"Request: {response.request.__dict__}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to make request: {e}")
            logger.error(f"Parsed error: {_parse_woo_error_json(response)}")
            raise

        except httpx.HTTPError as e:
            logger.error(f"Failed to make request: {e}")
            raise

        return response

    def get_json(self, endpoint: str, **kwargs: URLParams) -> dict[str, t.Any]:
        """
        Get JSON from the API.

        :param endpoint: The endpoint to request.
        :param kwargs: Additional keyword arguments.
        :return: The JSON response.
        """

        response = self._request(endpoint, "get", None, **kwargs)

        return response.json()

    def get(
        self, endpoint: str, expected_model: t.Type[T], **kwargs: URLParams
    ) -> T | None:
        """
        Get a model from the API.

        :param endpoint: The endpoint to request.
        :param expected_model: The model to expect.
        :param kwargs: Additional keyword arguments.
        :return: The model.
        """
        try:
            response = self.get_json(endpoint, **kwargs)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

        return expected_model.model_validate(response)

    def get_all(
        self, endpoint: str, expected_model: t.Type[T], follow_pages: bool = False, **kwargs: URLParams
    ) -> list[T]:
        """
        Get all models from the API.

        :param endpoint: The endpoint to request.
        :param expected_model: The model to expect.
        :param follow_pages: Whether to automatically follow pagination and get all pages. Defaults to False.
        :param kwargs: Additional keyword arguments.
        :return: The models.
        """
        if not follow_pages:
            response = self.get_json(endpoint, **kwargs)
            return [expected_model.model_validate(item) for item in response]
            
        # Follow pagination
        all_items = []
        current_page = 1
        
        # Make sure we're not overriding an existing page parameter
        if "page" in kwargs:
            current_page = int(kwargs["page"])
            
        # Create a copy of kwargs to modify for pagination
        page_kwargs = dict(kwargs)
        
        while True:
            page_kwargs["page"] = current_page
            
            # Make the request for the current page
            response = self._request(endpoint, "get", None, **page_kwargs)
            
            # Add items from the current page
            items = response.json()
            if not items:
                break
                
            all_items.extend(items)
            
            # Check if there are more pages using the Link header
            if "Link" not in response.headers:
                break
                
            # Check if there's a "next" relation in the Link header
            link_header = response.headers["Link"]
            if 'rel="next"' not in link_header:
                break
                
            # Move to the next page
            current_page += 1
            
            logger.debug(f"Following pagination to page {current_page}")
            
        return [expected_model.model_validate(item) for item in all_items]

    def post(self, endpoint: str, data: T, **kwargs: URLParams) -> T:
        """
        Post a model to the API.

        :param endpoint: The endpoint to request.
        :param data: The data to send.
        :param kwargs: Additional keyword arguments.
        :return: The response.
        """

        response = self._request(endpoint, "post", data, **kwargs)

        return data.__class__.model_validate(response.json())

    def put(self, endpoint: str, data: T, **kwargs: URLParams) -> T:
        """
        Put a model to the API.

        :param endpoint: The endpoint to request.
        :param data: The data to send.
        :param kwargs: Additional keyword arguments.
        :return: The response.
        """

        response = self._request(endpoint, "put", data, **kwargs)

        return data.__class__.model_validate(response.json())

    def delete(self, endpoint: str, **kwargs: URLParams) -> None:
        """
        Delete a model from the API.

        :param endpoint: The endpoint to request.
        :param kwargs: Additional keyword arguments.
        :return: The response.
        """

        response = self._request(endpoint, "delete", None, **kwargs)
