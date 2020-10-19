""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/shop/Resources/OrderSearch.html
"""
from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class OrderSearch(Endpoint):
    """OrderSearch Endpoint

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance (str, optional): Override the instance set in the client session. Defaults to None.
        site (str): Use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, site: str, instance: str = None):
        self.base = "order_search"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def Search(self, body, headers: dict = {}, **kwargs) -> Response:
        """Get Orders by Search query.

        [extended_summary]

        Args:
            body (dict): Dictionary for the POST request body.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """

        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}"
        return Endpoint.POST(self, url=url, body=body, headers=headers, idempotent=True)
