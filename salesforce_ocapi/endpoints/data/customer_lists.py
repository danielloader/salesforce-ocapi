""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/CustomerLists.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class CustomerLists(Endpoint):
    """CustomerLists Endpoint

    [extended_summary]

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "customer_lists"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def CustomerSearch(
        self, body: dict, customer_list_id: str, headers: dict = None, **kwargs,
    ) -> Response:
        """Get customer by search.

        [extended_summary]

        Args:
            body (dict): Dictionary for the POST request body.
            customer_list_id (str): Customer list ID.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{customer_list_id}/customer_search"
        return Endpoint.POST(self, url, body, headers=headers, idempotent=True)
