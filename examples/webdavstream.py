from salesforce_ocapi.auth import CommerceCloudClientSession, Profile
from salesforce_ocapi.endpoints import WebDAV


# get data via client credentials grant
credentials = Profile().read("default")
session = CommerceCloudClientSession(
    **credentials, instance="https://dev15-eu01-example.demandware.net"
)

WebDAVSession = WebDAV(session)


for x in WebDAVSession.StreamDirectoryList(
    "/on/demandware.servlet/webdav/Sites/Impex/src/instance/upload",
    get_info=True,
    count=10,
):
    print(x.path)
    # print(WebDAVSession.Delete(x.path))
