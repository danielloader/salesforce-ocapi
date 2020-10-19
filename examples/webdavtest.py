from salesforce_ocapi.auth import CommerceCloudClientSession, Profile
from salesforce_ocapi.endpoints import WebDAV


# get data via client credentials grant
credentials = Profile().read("default")
session = CommerceCloudClientSession(
    **credentials, instance="https://dev15-eu01-example.demandware.net"
)

# initalise an access token and renewal session
WebDAVSession = WebDAV(session)

# use credentials to upload a local folder recursively to the remote endpoint
WebDAVSession.Upload(
    local_filepath="examples/testfiles",
    remote_filepath="/on/demandware.servlet/webdav/Sites/Impex/src/instance/test-upload/",
)

# print directory listing to confirm upload has been successful
print(
    WebDAVSession.GetDirectoryList(
        "/on/demandware.servlet/webdav/Sites/Impex/src/instance/test-upload"
    )
)

# download file from webdav to local file path
# allows renaming the file in transit so the destination path locally needs the filename
WebDAVSession.Download(
    local_filepath="examples/example.xml",
    remote_filepath="on/demandware.servlet/webdav/Sites/Impex/src/instance/test-upload/example.xml",
)

# open the file locally in python and print contents to terminal
with open("examples/example.xml") as file:
    print(file.read())

# delete file on remote filepath
WebDAVSession.Delete(
    remote_filepath="/on/demandware.servlet/webdav/Sites/Impex/src/instance/test-upload/example.xml"
)

# repeat directory listing to confirm deletion visually
print(
    WebDAVSession.GetDirectoryList(
        "/on/demandware.servlet/webdav/Sites/Impex/src/instance/test-upload/"
    )
)


# altneratively stream the content from server to buffer to string in one move
print(
    WebDAVSession.StreamDownload(
        remote_filepath="on/demandware.servlet/webdav/Sites/Impex/src/instance/test-upload/example2.xml",
        decode=True,
    )
)
