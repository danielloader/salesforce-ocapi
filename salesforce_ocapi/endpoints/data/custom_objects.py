""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/CustomObjects.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class CustomObjects(Endpoint):
    """CustomObjects

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "custom_objects"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetCustomObject(
        self, object_type: str, key: str, headers: dict = None
    ) -> Response:
        """Get Custom Object by Key.

        [extended_summary]

        Args:
            object_type (str): Object type to get information about.
            key (str): Object key to get information about.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{object_type}/{key}"
        return Endpoint.GET(self, url, headers=headers)

    def PutCustomObject(
        self, object_type: str, key: str, body: dict, headers: dict = None
    ) -> Response:
        """Put Custom Object by Key.

        [extended_summary]

        Args:
            object_type (str): Object type to get information about.
            key (str): Object key to get information about.
            body (dict): Payload to send.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{object_type}/{key}"
        return Endpoint.PUT(self, url, headers=headers)

    def DeleteCustomObject(
        self, object_type: str, key: str, headers: dict = None
    ) -> Response:
        """Delete Custom Object by Key.

        [extended_summary]

        Args:
            object_type (str): Object type to delete.
            key (str): Object key to delete.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{object_type}/{key}"
        return Endpoint.DELETE(self, url, headers=headers)

    def PatchCustomObject(
        self, object_type: str, key: str, body: dict, headers: dict = None
    ) -> Response:
        """Patch Custom Object by Key.

        [extended_summary]

        Args:
            object_type (str): Object type to get information about.
            key (str): Object key to get information about.
            body (dict): Payload to patch object withs.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{object_type}/{key}"
        return Endpoint.PATCH(self, url, headers=headers)
