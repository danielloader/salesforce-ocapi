""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/shop/Resources/Orders.html
"""
from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class Orders(Endpoint):
    """Orders Endpoint

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "orders"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetOrder(self, order, headers: dict = {}) -> Response:
        """Get order.

        Args:
            order (str): String of the order number.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{order}"
        return Endpoint.GET(self, url=url, headers=headers)

    def PatchOrder(self, order, body, headers: dict = {}) -> Response:
        """Edit order.

        Args:
            order (str): String of the order number.
            body (dict): Body payload.

        Returns:
            Response: HTTPX response object.
        """

        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{order}"
        return Endpoint.PATCH(self, url=url, body=body, headers=headers)

    def AddOrderNote(self, order: str, note: dict, headers: dict = {}) -> Response:
        """Get order notes.

        Args:
            order (str): String of the order number.
            note (dict): Refer to Note Request document.

        Returns:
            Response: HTTPX response object
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{order}/notes"
        return Endpoint.POST(self, url=url, body=note, headers=headers)

    def GetOrderNotes(self, order: str, headers: dict = {}) -> Response:
        """Get order notes.

        Args:
            order (str): String of the order number.

        Returns:
            Response: HTTPX response object
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{order}/notes"
        return Endpoint.GET(self, url=url, headers=headers)

    def DeleteOrderNote(self, order: str, note: str, headers: dict = {}) -> Response:
        """Delete order note.

        Args:
            order (str): String of the order number.
            note (str): ID of note to delete.

        Returns:
            Response: HTTPX response object
        """
        url = f"{self.instance}/s/{self.site}/dw/shop/v20_4/{self.base}/{order}/notes/{note}"
        return Endpoint.DELETE(self, url=url, headers=headers)
