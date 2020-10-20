""" Helper methods for doing HTTP requests.
"""
from httpcore import _exceptions
from httpx import Client, Response
from opnieuw import RetryException, retry

from salesforce_ocapi.utils.decorators import basicauth, contenttype
from salesforce_ocapi.utils.exceptions import IdempotentTimeout


class Request:
    """Start a requests session and provide helper methods for HTTP verbs.
    """

    def __init__(self):
        self.session = Client(timeout=10)
        self.headers = self.client.AuthHeader

    def InjectAttrs(self, **kwargs):
        """Add custom headers if requested, default authorisation header included in __init__.

        Args:
            headers (dict): Key value pairs for headers
        """
        if kwargs.get("headers"):
            self.headers = {**self.headers, **kwargs.get("headers")}
        if kwargs.get("start"):
            self.body.update({"start": kwargs.get("start")})

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    @basicauth
    def GET(self, url, params={}, headers: dict = {}) -> Response:
        """HTTP GET Request

        Args:
            url (str): URL to connect to.
            headers (dict, optional): Key Value pairs for additional headers. (default: None)

        Returns:
            Response -- HTTPX Response object
        """
        self.InjectAttrs(headers=headers)
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            return response
        except _exceptions.TimeoutException:
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    @contenttype
    @basicauth
    def PATCH(
        self, url: str, body=None, headers: dict = {}, idempotent: bool = False,
    ) -> Response:
        """HTTP PATCH Request

        Args:
            url (str): URL to connect to.
            body (dict, optional): JSON payload for the request. (default: dict())
            headers (dict, optional): Key Value pairs for additional headers. (default: None)
            idempotent (bool, optional): Is this request idempotent? (default: False)

        Returns:
            Response -- HTTPX Response object
        """
        self.InjectAttrs(headers=headers)
        try:
            response = self.session.patch(url, data=body, headers=self.headers)
            return response
        except _exceptions.TimeoutException:
            if idempotent is False:
                raise IdempotentTimeout(
                    method="PATCH", url=url, data=body, headers=self.headers
                )
            else:
                print("retry")
                raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    @contenttype
    @basicauth
    def PUT(self, url: str, body: dict = {}, headers: dict = {}) -> Response:
        """HTTP PUT Request

        Args:
            url (str): URL to connect to.
            body (dict, optional): JSON payload for the request. (default: dict())
            headers (dict, optional): Key Value pairs for additional headers. (default: None)

        Returns:
            Response -- HTTPX Response object
        """
        self.InjectAttrs(headers=headers)
        try:
            response = self.session.put(url, data=body, headers=self.headers)
            return response
        except _exceptions.TimeoutException:
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    @contenttype
    @basicauth
    def POST(
        self,
        url: str,
        body: str = None,
        params: dict = None,
        headers: dict = {},
        idempotent: bool = False,
    ) -> Response:
        """HTTP POST Request

        Args:
            url (str): URL to connect to.
            body (dict, optional): JSON payload for the request. (default: dict())
            params (dict, optional): Dictionary for path parameters. (default: None)
            headers (dict, optional): Key Value pairs for additional headers. (default: None)
            idempotent (bool, optional): Is this request idempotent? (default: False)

        Returns:
            Response -- HTTPX Response object
        """
        self.InjectAttrs(headers=headers)
        try:
            response = self.session.post(
                url, body=body, params=params, headers=self.headers
            )
            return response
        except _exceptions.TimeoutException:
            if idempotent is False:
                raise IdempotentTimeout(
                    method="POST", url=url, body=body, headers=self.headers
                )
            else:
                print("retry")
                raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    @contenttype
    @basicauth
    def DELETE(self, url: str, body: dict = {}, headers: dict = {}) -> Response:
        """HTTP DELETE Request

        Args:
            url (str): URL to connect to.
            body (dict, optional): JSON payload for the request. (default: dict())
            headers (dict, optional): Key Value pairs for additional headers. (default: None)

        Returns:
            Response -- HTTPX Response object
        """
        self.InjectAttrs(headers=headers)
        try:
            response = self.session.delete(url, headers=self.headers)
            return response
        except _exceptions.TimeoutException:
            raise RetryException


class Endpoint(Request):
    """Endpoint base class, sets auth client, site variable and instance variable for URLs.

    Args:
        Request (HTTP Verb): Which HTTP method to call from Request class.
    """

    def __init__(self, client, instance=None, site="-"):
        self.client = client
        self.site = site
        self.instance = instance or self.client.instance
        super().__init__()
