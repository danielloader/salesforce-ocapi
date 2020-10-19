""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Resources/Jobs.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class Jobs(Endpoint):
    """Jobs

    Args:
        client (CommerceCloudBMToken): Business Manager authenticated session token.
        instance ([type], optional): Override the instance set in the client session. Defaults to None.
        site (str, optional): Optionally use site specific context instead of global. Defaults to "-".
    """

    def __init__(self, client, instance=None, site="-"):
        self.base = "jobs"
        super().__init__(client, instance, site)

    def __repr__(self):
        return self.__class__.__name__

    def GetJobExecution(self, job_id: str, id: str, headers: dict = None) -> Response:
        """Get Job Execution information by Execution ID for Job ID.

        [extended_summary]

        Args:
            job_id (str): Job ID to get information about.
            id (str): Execution ID to get information about.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{job_id}/executions/{id}"
        return Endpoint.GET(self, url, headers=headers)

    def DeleteJobExecution(
        self, job_id: str, id: str, headers: dict = None
    ) -> Response:
        """Delete Job Execution by Execution ID for Job ID.

        [extended_summary]

        Args:
            job_id (str): Job ID to get information about.
            id (str): Execution ID to get information about.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{job_id}/executions/{id}"
        return Endpoint.DELETE(self, url, headers=headers)

    def ExecuteJob(self, job_id: str, headers: dict = None) -> Response:
        """Trigger Job Execution information by Job ID.

        [extended_summary]

        Args:
            job_id (str): Job ID to get information about.
            id (str): Execution ID to get information about.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/{job_id}/executions"
        return Endpoint.POST(self, url, headers=headers)
