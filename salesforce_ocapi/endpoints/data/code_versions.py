""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/CodeVersions.html
"""

from httpx._models import Response

from salesforce_ocapi.auth.helper import BaseToken
from salesforce_ocapi.utils import Endpoint


class CodeVersions(Endpoint):
    """CodeVersions Endpoint

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "code_versions"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetCodeVersions(self, headers: dict = None) -> Response:
        """Get Code Versions on Commerce Cloud Instance.

        [extended_summary]

        Args:
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """

        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}"
        return Endpoint.GET(self, url, headers=headers)

    def PutCodeVersions(self, code_version_id: str, headers: dict = None):
        """Create code version.

        Args:
            code_version_id (str): Code Version to create.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """

        url = (
            f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{code_version_id}"
        )
        return Endpoint.PUT(self, url, headers=headers)

    def PatchCodeVersions(self, code_version_id: str, body: dict, headers: dict = None):
        """Patch code version.

        Update an existing code version.

        Notes:
            Only an inactive code version can be updated.
            Only the active flag and the id can be changed. The active flag can therefore only set to "true".
            To set the active flag to "false" will not work.

        Args:
            code_version_id (str): Code Version to create.
            body (dict): Options to patch code version.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """

        url = (
            f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{code_version_id}"
        )
        return Endpoint.PATCH(self, url, headers=headers)

    def GetCodeVersion(self, code_version_id: str, headers: dict = None) -> Response:
        """Get Code Version on Commerce Cloud Instance.

        Args:
            code_version_id (str): Code Version to get information about.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """

        url = (
            f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{code_version_id}"
        )
        return Endpoint.GET(self, url, headers=headers)

    def DeleteCodeVersion(self, code_version_id: str, headers: dict = None) -> Response:
        """Delete Code Version on Commerce Cloud Instance.

        Args:
            code_version_id (str): Code Version to delete.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """

        url = (
            f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{code_version_id}"
        )
        return Endpoint.DELETE(self, url, headers=headers)
