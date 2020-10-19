from salesforce_ocapi.auth import CommerceCloudClientSession, Profile
from salesforce_ocapi.endpoints import CodeVersions
from salesforce_ocapi.utils.fs import Zipper

PRODUCTION = [
    "https://staging-eu01-example.demandware.net",
    "https://development-eu01-example.demandware.net",
    "https://production-eu01-example.demandware.net",
]

SANDBOXES = [
    "https://dev01-eu01-example.demandware.net",
    "https://dev02-eu01-example.demandware.net",
    "https://dev03-eu01-example.demandware.net",
    "https://dev04-eu01-example.demandware.net",
    "https://dev05-eu01-example.demandware.net",
    "https://dev07-eu01-example.demandware.net",
    "https://dev08-eu01-example.demandware.net",
    "https://dev09-eu01-example.demandware.net",
    "https://dev10-eu01-example.demandware.net",
    "https://dev11-eu01-example.demandware.net",
    "https://dev12-eu01-example.demandware.net",
    "https://dev13-eu01-example.demandware.net",
    "https://dev14-eu01-example.demandware.net",
    "https://dev15-eu01-example.demandware.net",
    "https://dev16-eu01-example.demandware.net",
    "https://dev17-eu01-example.demandware.net",
    "https://dev18-eu01-example.demandware.net",
    "https://dev19-eu01-example.demandware.net",
    "https://dev20-eu01-example.demandware.net",
    "https://dev21-eu01-example.demandware.net",
    "https://dev22-eu01-example.demandware.net",
]

credentials = Profile().read()
session = CommerceCloudClientSession(
    **credentials, instance="https://dev01-eu01-example.demandware.net"
)


for sandbox in SANDBOXES:
    codeversions = CodeVersions(session, instance=sandbox).GetCodeVersions()
    print(sandbox, codeversions)
