""" Request paginator helper, takes request, gets response and checks for pages, returns all pages.
"""
from urllib import parse

import jmespath
from tqdm import tqdm

from salesforce_ocapi.utils.exceptions import (
    NotOCAPIEndpoint,
    OCAPIMethodNotFound,
    PaginatorProgressHidden,
)


class Paginator:
    """Paginator

    Paginator helper that returns pages from paginated GET and POST requests.

    Args:
        endpoint (Endpoint Object): OCAPI endpoint object from this library.
        method (str): Name of method in the endpoint object to call.

    Raises:
        NotOCAPIEndpoint: Endpoint given is not an OCAPI endpoint object.
        OCAPIMethodNotFound: Method given is not included in Endpoint object given.
    """

    def __init__(self, endpoint, method, progress: bool = False, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        if progress:
            self.pbar = tqdm(total=0, position=0)
        else:
            self.pbar = tqdm(disable=True)

        try:
            assert hasattr(endpoint, "base")
            self._endpoint = endpoint
        except AssertionError:
            raise NotOCAPIEndpoint(endpoint)
        try:
            assert hasattr(self._endpoint, method)
            self._method = getattr(self._endpoint, method)
        except AssertionError:
            raise OCAPIMethodNotFound(endpoint, method)

    def _get_pages(self, params=None, *args, **kwargs):
        """Get Pages

        Private method to handle getting and yielding pages until exhaustion.

        Yields:
            response.json(): HTTPX response json() representation of the page.
        """
        args = self._args
        kwargs = {**self._kwargs, **kwargs}

        if "body" in kwargs:
            selections = kwargs["body"].get("select")[1:-1].split(",")
            selections.extend(["next", "count", "total"])
            selections = list(set(selections))
            kwargs["body"]["select"] = f'({",".join(selections)})'
            try:
                if "count" in params:
                    kwargs["body"]["count"] = params["count"]
            except TypeError:
                pass
        response = self._method(params=params, *args, **kwargs)
        r = response.json()
        if len(r.get("hits", [])) == 0:
            yield r
            self.pbar.close()
            return
        self.pbar.total = r["total"]
        self.pbar.update(len(r["hits"]))
        yield r
        if response.request.method == "POST":
            while r.get("next"):
                kwargs["body"]["start"] = r["next"]["start"]
                response = self._method(*args, **kwargs)
                r = response.json()
                if r.get("hits"):
                    self.pbar.update(len(r["hits"]))
                    yield r
        if response.request.method == "GET":
            while r.get("next"):
                params = parse.parse_qs(parse.urlsplit(r["next"]).query)
                response = self._method(params=params, *args, **kwargs)
                r = response.json()
                if r.get("hits"):
                    self.pbar.update(len(r["hits"]))
                    yield r
        self.pbar.close()

    def write(self, message):
        if self.pbar.disable is True:
            raise PaginatorProgressHidden
        else:
            self.pbar.write(message)

    def search(self, search_string: str, *args, **kwargs):
        """Search in response JSON.

        Filters response JSON using JMESPath queries.

        Args:
            search_string (str): JMESPath query.

        Yields:
            dict: Filtered JSON.
        """
        expression = jmespath.compile(search_string)
        for result in self._get_pages(*args, **kwargs):
            if result.get("hits"):
                yield expression.search(result)

    def paginate(self, *args, **kwargs):
        """Pagination method for class.

        Wrapper around the _get_pages method.

        Yields:
            response.json(): HTTPX response json() representation of the page.
        """
        yield from self._get_pages(*args, **kwargs)

    def hits(self, *args, **kwargs):
        """Hits only pagination method.

        Only returns the hits in the responses. Useful if you don't need additional
        fields in a response.

        Yields:
            dict: Each "hit" object decoded from JSON.
        """
        for result in self._get_pages(*args, **kwargs):
            if result.get("hits"):
                for _ in result["hits"]:
                    yield _
     
