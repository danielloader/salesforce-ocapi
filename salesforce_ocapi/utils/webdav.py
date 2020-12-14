from datetime import datetime as dt
from hashlib import md5
from pathlib import Path

from opnieuw import RetryException, retry
from webdav3.exceptions import (
    ConnectionException,
    NoConnection,
    RemoteResourceNotFound,
    WebDavException,
)

import pytz


@retry(
    retry_on_exceptions=(RetryException),
    max_calls_total=10,
    retry_window_after_first_call_in_seconds=60,
)
def s3_compare(
    client, webdav: dict, webdav_prefix: str, s3: dict, s3_prefix: str
) -> dict:
    """Compare WebDAV resource with AWS S3 bucket hosted resource.

    Args:
        client (WebDAVClientSession): Client session from Salesforce OCAPI library.
        webdav (dict): Collection of resource information from WebDAV.
        webdav_prefix (str): Prefix from the root of the WebDAV host to the base path for the accessible files.
        s3 (dict): Collection of resource information from AWS S3 bucket key.
        s3_prefix (str): Prefix from the root of the S3 Bucket to the base path for the accessible files.

    Raises:
        RetryException: Increment the retry attempts to the max_calls_total specified in the decorator.

    Returns:
        dict: Dictionary of comparison of the two objects, including boolean to indicate matching status.
    """
    client.reauth()
    webdav["size"] = int(webdav["size"])
    filepath = client.hostname + webdav["path"]
    try:
        # Modified times are sometimes already in ISO8601... don't ask.
        webdav["modified"] = (
            dt.strptime(webdav["modified"], "%a, %d %b %Y %H:%M:%S %Z")
            .replace(tzinfo=pytz.utc)
            .isoformat()
        )
    except ValueError:
        pass
    etag = s3.e_tag[1:-1]
    try:
        if "-" not in etag:
            # Compute regular MD5 hash on file buffer
            sum = md5(client.StreamDownload(webdav["path"]).getbuffer())

            hashsum = sum.hexdigest()

        if "-" in etag:
            # This function relies on the default chunksize on s3 via the aws cli (8MB)
            # WARNING: Anything else will fail
            md5s = []
            chunk_size = 8 * 1024 * 1024
            f = client.StreamDownload(webdav["path"])
            for data in iter(lambda: f.read(chunk_size), b""):
                md5s.append(md5(data))
            f.close()
            digests = b"".join(m.digest() for m in md5s)
            digests_md5 = md5(digests)
            hashsum = "{}-{}".format(digests_md5.hexdigest(), len(md5s))

        webdav.update({"hashsum": hashsum})
        webdav = dict(sorted(webdav.items()))
        s3_data = {
            "hashsum": etag,
            "modified": s3.last_modified.isoformat(),
            "name": str(Path(s3.key).name),
            "path": s3.key,
            "size": s3.content_length,
        }

        comparison = {
            "webdav": webdav,
            "s3": s3_data,
            "filepath": filepath,
            "match": (lambda a, b: a["hashsum"] == b["hashsum"])(webdav, s3_data),
        }

        return comparison

    except (NoConnection, ConnectionException, WebDavException, RemoteResourceNotFound):
        client.reconnect()
        raise RetryException
