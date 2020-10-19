""" https://documentation.b2c.commercecloud.salesforce.com/DOC1/topic/com.demandware.dochelp/ImportExport/UsingWebDAV.html
"""
import time
from hashlib import md5
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

from opnieuw import RetryException, retry
from webdav3.client import Client
from webdav3.exceptions import ConnectionException, NoConnection, WebDavException


class WebDAV:
    """Commerce Cloud WebDAV session.

    [extended_summary]

    Args:
        client (CommerceCloudClientSession): Active client session with Commerce Cloud for a bearer token.
        instance (str, optional): Optional commerce cloud instance, useful for opening clients to multiple instances using the same bearer token. Defaults to None.
        cert (str, optional): Path to TLS client certificate. Defaults to None.
        key ([type], optional): Export key for the TLS certificate. Defaults to None.
        verify (bool, optional): Verify TLS certificates, set to false for self signed. Defaults to True.
    """

    def __init__(self, client, instance=None, cert=None, key=None, verify=True):
        self.client = client

        self._instance = instance or self.client.instance
        self.options = {"webdav_hostname": self._instance.rstrip("/")}
        self.verify = verify
        self.token = self.client.Token
        self.options.update({"webdav_token": self.token["access_token"]})
        self.webdav_client = Client(self.options)
        self.webdav_client.verify = self.verify
        if cert and key:
            self.cert = str(Path(cert).resolve())
            self.key = str(Path(key).resolve())
            self.options.update({"cert_path": self.cert, "key_path": self.key})

    def reauth(self):
        """Checks token expiry and re-initialises the Client if a new token is needed.
        """
        if self.token["expires_at"] < int(time.time()):
            self.client.getToken()
            self.options.update({"webdav_token": self.token["access_token"]})
            self.webdav_client = Client(self.options)

    def reconnect(self):
        """Re-initalise the Client session.
        """
        self.webdav_client = Client(self.options)

    @property
    def hostname(self):
        """Return the hostname the WebDAV client connection is connected to.

        Returns:
            str: Hostname including prefix eg https://
        """
        return self.options["webdav_hostname"]

    @property
    def netloc(self):
        """Return a urlparse netloc string of the connected hostname.

        Returns:
            str: netloc of hostname.
        """
        url = urlparse(self.options["webdav_hostname"])
        return url.netloc

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def GetInfo(self, remote_filepath: str, headers: dict = None) -> list:
        """Get properties for entity

        [extended_summary]

        Args:
            remote_filepath (str): Path to remote resource.
            headers (dict, optional): Additional headers to apply to request. Defaults to None.

        Raises:
            RetryException: Adds to retries counter on failure.

        Returns:
            list: WebDAV attribute information.
        """
        try:
            return self.webdav_client.info(remote_filepath)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def GetDirectoryList(
        self, filepath: str, get_info: bool = False, headers: dict = None
    ) -> list:
        """Get list of files and folders in a path from WebDAV endpoint.

        [extended_summary]

        Args:
            filepath (str): Path to get directory listing for.
            get_info (bool): returns dictionary of attributes instead of file list.
            headers (dict, optional): Additional headers to apply to request. Defaults to None.

        Returns:
            list: Directory listing.
        """
        try:
            return self.webdav_client.list(filepath, get_info=get_info)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def Upload(self, local_filepath: str, remote_filepath: str):
        """Upload file or directory recursively to WebDAV endpoint.

        [extended_summary]

        Args:
            local_filepath (str): Local path to file or directory to upload.
            remote_filepath (str): Remote path to upload to.
        """
        local_filepath = str(Path(local_filepath).resolve())
        try:
            self.webdav_client.upload_sync(remote_filepath, local_filepath)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def StreamUpload(self, payload, remote_path: str, file_name: str):
        """Upload FileIO, StringIO, BytesIO or string to WebDAV

        [extended_summary]

        Args:
            payload: Stream payload
            remote_path (str): Remote path relative to host.
            file_name (str): Name for the file uploaded.
        """
        try:
            self.webdav_client.upload_to(payload, f"{remote_path}/{file_name}")
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def MakeDir(self, remote_path: str):
        """Make new directory at path specified.

        Args:
            remote_path (str): Path of proposed new directory.
        """
        try:
            self.webdav_client.mkdir(remote_path)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def Move(
        self, remote_path_source: str, remote_path_dest: str, overwrite: bool = False
    ):
        """Make new directory at path specified.

        Args:
            remote_path_source (str): Path of source resource.
            remote_path_dest (str): Path of destination resource.
            overwrite (bool): Overwrite destination resource. Defaults to False.
        """
        try:
            self.webdav_client.move(remote_path_source, remote_path_dest, overwrite)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def Delete(self, remote_filepath: str):
        """Delete file on remote WebDAV endpoint.

        Args:
            remote_filepath (str): Location of resource to delete.
        """
        try:
            self.webdav_client.clean(remote_filepath)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def Download(self, local_filepath: str, remote_filepath: str):
        """Download file/folder from WebDAV endpoint.

        This is a synchronous operation, and the file is downloaded in full to the local_filepath.

        Args:
            local_filepath (str): Local path to download to, including filename of file saved.
            remote_filepath (str): Remote path to file to download.
        """
        local_filepath = str(Path(local_filepath).resolve())
        try:
            self.webdav_client.download_sync(remote_filepath, local_filepath)
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def Pull(self, local_filepath: str, remote_filepath: str):
        """Sync file/folder from WebDAV endpoint to local storage.

        This downloads missing or nwer modified files from the remote to local storage.
        You can use it to do "resumeable" transfers, but the checks are slow for deeply nested files.

        Args:
            local_filepath (str): Local path to download to, including filename of file saved.
            remote_filepath (str): Remote path to file to download.
        """
        local_filepath = str(Path(local_filepath).resolve())
        try:
            self.webdav_client.pull(remote_filepath, local_filepath)
            return True
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException
        return False

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=3,
        retry_window_after_first_call_in_seconds=10,
    )
    def Push(self, local_filepath: str, remote_filepath: str):
        """Sync file/folder from local storage to WebDAV endpoint.

        This uploads missing or nwer modified files from the local to remote storage.
        You can use it to do "resumeable" transfers, but the checks are slow for deeply nested files.

        Args:
            local_filepath (str): Local path to download to, including filename of file saved.
            remote_filepath (str): Remote path to file to download.
        """
        local_filepath = str(Path(local_filepath).resolve())
        try:
            self.webdav_client.push(local_filepath, remote_filepath)
            return True
        except (NoConnection, ConnectionException, WebDavException):
            self.reauth()
            raise RetryException
        return False

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=10,
        retry_window_after_first_call_in_seconds=15,
    )
    def StreamDownload(self, remote_filepath: str, buffer=None, decode: bool = False):
        """Download a file in chunks to a local file buffer.

        You must provide a BytesIO object or one will be created for you.

        Args:
            remote_filepath (str): Path to remote resource to download.
            buffer ([type], optional): Buffer write streamed content to.
            decode (bool, optional): Optionally try to decode downloaded file into a string. Defaults to False.

        Raises:
            RetryException: Adds to retries counter on failure.

        Returns:
            Bytes: Returns a BytesIO object for further use.
        """
        self.reauth()
        if buffer is None:
            buffer = BytesIO()
        try:
            self.webdav_client.download_from(buff=buffer, remote_path=remote_filepath)
            if decode is True:
                return buffer.getvalue().decode("utf-8")
            else:
                buffer.seek(0)
                return buffer
        except (NoConnection, ConnectionException, WebDavException):
            raise RetryException

    @retry(
        retry_on_exceptions=(RetryException),
        max_calls_total=10,
        retry_window_after_first_call_in_seconds=60,
    )
    def HashObject(self, remote_filepath: str) -> str:
        """Generate a MD5 hashsum for a remote resource.

        This is streamed into memory, hashed and discarded. Optimised for low memory but
        high bandwidth environments.

        Args:
            remote_filepath (str): Path to remote resource.

        Raises:
            RetryException: Adds to retries counter on failure.

        Returns:
            str: MDSSUM of the file requested.
        """
        self.reauth()
        try:
            sum = md5(self.StreamDownload(remote_filepath).getbuffer())
            return {
                "filepath": remote_filepath,
                "hashtype": "MD5",
                "hashsum": sum.hexdigest(),
            }

        except (NoConnection, ConnectionException, WebDavException):
            self.reconnect()
            raise RetryException

    def RecursiveFileListing(self, remote_filepath: str) -> str:
        """Recursive filetree walker, returns paths found.

        Args:
            remote_filepath (str): [description]

        Raises:
            RetryException: Adds to retries counter on failure.

        Yields:
            Iterator[str]: Yields resource paths for any files found.
        """

        @retry(
            retry_on_exceptions=(RetryException),
            max_calls_total=10,
            retry_window_after_first_call_in_seconds=60,
        )
        def get_list(self, path):
            self.reauth()
            try:
                return self.webdav_client.list(path, get_info=True)
            except (NoConnection, ConnectionException, WebDavException):
                self.reconnect()
                raise RetryException

        def get_files(self, path):
            return [x for x in get_list(self, path) if x["isdir"] is False]

        def get_dirs(self, path):
            return [x["path"] for x in get_list(self, path) if x["isdir"] is True]

        yield from get_files(self, remote_filepath)
        for subdir in get_dirs(self, remote_filepath):
            yield from self.RecursiveFileListing(subdir)

    def RecursiveFolderListing(self, remote_filepath: str) -> str:
        """Recursive filetree walker, returns paths found.

        Args:
            remote_filepath (str): [description]

        Raises:
            RetryException: Adds to retries counter on failure.

        Yields:
            Iterator[str]: Yields resource paths for any files found.
        """

        @retry(
            retry_on_exceptions=(RetryException),
            max_calls_total=10,
            retry_window_after_first_call_in_seconds=60,
        )
        def get_list(self, path):
            self.reauth()
            try:
                return self.webdav_client.list(path, get_info=True)
            except (NoConnection, ConnectionException, WebDavException):
                self.reconnect()
                raise RetryException

        def get_dirs(self, path):
            return [x["path"] for x in get_list(self, path) if x["isdir"] is True]

        dirlist = get_dirs(self, remote_filepath)

        yield from dirlist
        for subdir in get_dirs(self, remote_filepath):
            yield from self.RecursiveFolderListing(subdir)
