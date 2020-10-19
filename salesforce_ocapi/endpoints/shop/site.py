""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/shop/Resources/Site.html
"""
from salesforce_ocapi.utils import Endpoint


class Site(Endpoint):
    """Site Endpoint

    [extended_summary]

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "site"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetSiteInformation(self, site: str = None, headers: dict = {}):
        """Get a Commerce Cloud order

        Arguments:
            order {str} -- String of the order number

        Returns:
            Response -- HTTPX response object
        """
        self.site = site or self.site
        headers.update({"x-dw-client-id": self.client.client_id})
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}"
        return Endpoint.GET(self, url, headers=headers)
