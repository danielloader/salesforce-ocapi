""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/JobExecutionSearch.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class JobExecutionSearch(Endpoint):
    """JobsExecutionSearch Endpoint

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "job_execution_search"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetJobExecution(self, body: dict, headers: dict = None, **kwargs) -> Response:
        """Get job execution by Job ID.

        [extended_summary]

        Args:
            body (dict): Dictionary for the POST request body.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}"
""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/JobExecutionSearch.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class JobExecutionSearch(Endpoint):
    """JobsExecutionSearch Endpoint

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "job_execution_search"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetJobExecution(self, body: dict, headers: dict = None, **kwargs) -> Response:
        """Get job execution by Job ID.

        [extended_summary]

        Args:
            body (dict): Dictionary for the POST request body.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}"
        print(type(body))
        print(body)
        return Endpoint.POST(self, url, body, headers=headers, idempotent=True)

