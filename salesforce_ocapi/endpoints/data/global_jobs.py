""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/SystemJobs/GlobalJobs.html
"""

from httpx._models import Response

from salesforce_ocapi.utils import Endpoint


class GlobalJobs(Endpoint):
    """GlobalJobs

    [extended_summary]

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

    def FullActiveDataIndexUpdate(
        self, site_scope: str, headers: dict = None
    ) -> Response:
        """Full Active Data Index Update.

        This job builds all active data related search indexes for the given site scope.

        Args:
            site_scope (str): Site scope to re-index.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-search-index-active-data-full-update/executions"
        body = {"site_scope": site_scope}
        return Endpoint.POST(self, url, body=body, headers=headers)

    def FullContentIndexUpdate(self, site_scope: str, headers: dict = None) -> Response:
        """Full Content Index Update.

        This job builds all content related search indexes for the given site scope.

        Args:
            site_scope (str): Site scope to re-index.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-search-index-content-full-update/executions"
        body = {"site_scope": site_scope}
        return Endpoint.POST(self, url, body=body, headers=headers)

    def FullProductIndexUpdate(self, site_scope: str, headers: dict = None) -> Response:
        """Full Product Index Update.

        This job builds all product related search indexes for the given site scope.

        Args:
            site_scope (str): Site scope to re-index.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-search-index-product-full-update/executions"
        body = {"site_scope": site_scope}
        return Endpoint.POST(self, url, body=body, headers=headers)

    def IncrementatlActiveDataIndexUpdate(
        self, site_scope: str, headers: dict = None
    ) -> Response:
        """Incremental Active Data Index Update.

        This job updates all active data related search indexes for the given site scope.

        Args:
            site_scope (str): Site scope to re-index.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-search-index-active-data-incremental-update/executions"
        body = {"site_scope": site_scope}
        return Endpoint.POST(self, url, body=body, headers=headers)

    def IncrementalContentIndexUpdate(
        self, site_scope: str, headers: dict = None
    ) -> Response:
        """Incremental Content Index Update.

        This job updates all content related search indexes for the given site scope.

        Args:
            site_scope (str): Site scope to re-index.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-search-index-content-incremental-update/executions"
        body = {"site_scope": site_scope}
        return Endpoint.POST(self, url, body=body, headers=headers)

    def IncrementalProductIndexUpdate(
        self, site_scope: str, headers: dict = None
    ) -> Response:
        """Incremental Product Index Update.

        This job updates all product related search indexes for the given site scope.

        Args:
            site_scope (str): Site scope to re-index.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-search-index-product-incremental-update/executions"
        body = {"site_scope": site_scope}
        return Endpoint.POST(self, url, body=body, headers=headers)

    def SiteArchiveExport(
        self,
        data_units: dict,
        file_path: str,
        overwrite: bool = False,
        headers: dict = None,
    ) -> Response:
        """Export XML ZIP file.

        This job is for executing a site export to an archive file based on data unit configuration in json format.
        https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/OCAPI/current/data/Documents/SiteArchiveExportConfiguration.html

        Args:
            data_units (dict): Dictionary defining the Export units to export.
            file_path (str): Path to zipfile to export, relative to Impex/src.
            overwrite (bool): Overwrite zipfile in export location. Defaults to False.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-site-archive-import/executions"
        body = {
            "export_file": file_path,
            "data_units": data_units,
            "overwrite_export_file": overwrite,
        }
        return Endpoint.POST(self, url, body=body, headers=headers)

    def SiteArchiveImport(
        self, file_path: str, mode: str = "merge", headers: dict = None
    ) -> Response:
        """Import XML ZIP file.

        This job is for importing a whole site import ZIP file. Note that the file is specified by its simple file name
        and must be already uploaded to the server. You may specify an import mode, where currently only 'merge' is supported.

        Args:
            file_path (str): Path to zipfile to import.
            mode (str): Mode to import XML, merge only supported option at this time.
            headers (dict, optional): Key value pairs for headers added to request. Defaults to None.

        Returns:
            Response: HTTPX response object.
        """
        url = f"{self.instance}/s/{self.site}/dw/data/v20_4/{self.base}/sfcc-site-archive-import/executions"
        body = {"file_name": file_path, "mode": mode}
        return Endpoint.POST(self, url, body=body, headers=headers)
