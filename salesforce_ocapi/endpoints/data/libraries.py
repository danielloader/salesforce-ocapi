""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/Libraries.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class Libraries(Endpoint):
    """Libraries

    [extended_summary]

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
            site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "libraries"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetContentAsset(
        self, library_id: str, content_id: str, headers: dict = None
    ) -> Response:
        """Get Content Asset by Content ID inside of a Library.

        Args:
            library_id (str): Content Library.
            content_id (str): Content Asset name.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{library_id}/content/{content_id}"
        return Endpoint.GET(self, url, headers=headers)

    def PutContentAsset(
        self, library_id: str, content_id: str, body: dict, headers: dict = None
    ) -> Response:
        """Put Content Asset by Content ID inside of a Library.

        Args:
            library_id (str): Content Library.
            content_id (str): Content Asset name.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{library_id}/content/{content_id}"
        return Endpoint.PUT(self, url, body, headers=headers)
