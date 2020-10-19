""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/shop/Resources/ProductSearch.html
"""
from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class ProductSearch(Endpoint):
    """ProductSearch Endpoint

    [extended_summary]

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance (str, optional): Override the instance set in the client session. Defaults to None.
        site (str): Use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, site: str, instance: str = None):
        self.base = "product_search"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def Search(self, params: dict, headers: dict = {}, **kwargs) -> Response:
        """Get Products by Search query.

        [extended_summary]

        Args:
            params (dict): Dictionary for the query param key value pairs.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        headers.update({"x-dw-client-id": self.client.client_id})
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}"
        return Endpoint.GET(self, url, params=params, headers=headers)
