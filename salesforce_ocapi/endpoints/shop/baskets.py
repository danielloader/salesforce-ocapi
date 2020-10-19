""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/shop/Resources/Baskets.html
"""
from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class Baskets(Endpoint):
    """Baskets Endpoint

    [extended_summary]

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "baskets"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def CreateBasket(self, headers=None) -> Response:
        """Create default basket.

        [extended_summary]

        Args:
            headers (dict, optional): Additional headers to inject. Defaults to None.

        Returns:
            Response: Response to request.
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}"
        return Endpoint.POST(self, url, headers=headers)

    def GetBasket(self, basket_id: str, headers=None) -> Response:
        """Get a basket.

        Args:
            basket_id (str): The unique identifier for the basket.
            headers (dict, optional): Additional headers to inject. Defaults to None.

        Returns:
            Response: Response to request.
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{basket_id}"
        return Endpoint.GET(self, url, headers=headers)

    def ModifyBasket(self, basket_id: str, body: dict, headers=None) -> Response:
        """Get a basket.

         Updates a basket. Only the currency of the basket, source code, and the custom
         properties of the basket and of the shipping items will be considered.

        Args:
            basket_id (str): The unique identifier for the basket.
            body (dict): Dictionary of key value pairs to modify order with.
            headers (dict, optional): Additional headers to inject. Defaults to None.

        Returns:
            Response: Response to request.
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{basket_id}"
        return Endpoint.PATCH(self, url, body, headers=headers)

    def DeleteBasket(self, basket_id: str, headers=None) -> Response:
        """Remove a basket.

        Args:
            basket_id (str): The unique identifier for the basket.
            headers (dict, optional): Additional headers to inject. Defaults to None.

        Returns:
            Response: Response to request.
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{basket_id}"
        return Endpoint.DELETE(self, url, headers=headers, idempotent=True)
