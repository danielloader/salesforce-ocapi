from salesforce_ocapi.auth import CommerceCloudBMSession, Profile
from salesforce_ocapi.endpoints import Site, WebDAV, GlobalJobs
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
site_info_session = CommerceCloudBMSession(
    **credentials, instance="https://dev01-eu01-example.demandware.net"
)


def fix_timezone(instance):
    timezone = "Europe/London"
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<preferences xmlns="http://www.demandware.com/xml/impex/preferences/2007-03-31">'
        "<standard-preferences>"
        "<all-instances>"
        f'<preference preference-id="SiteTimezone">{timezone}</preference>'
        "</all-instances>"
        "</standard-preferences>"
        "</preferences>"
    )

    payload = Zipper()
    payload.add(
        payload=xml, relative_path="timezonefix/sites/sitegenesis/preferences.xml"
    )
    session = CommerceCloudBMSession(**credentials, instance=instance)
    WebDAV(client=session).UploadStream(
        payload=payload.stream,
        remote_path="/on/demandware.servlet/webdav/Sites/Impex/src/instance/",
        file_name="timezonefix.zip",
    )
    print(GlobalJobs(client=session).SiteArchiveImport(file_path="timezonefix.zip"))


for sandbox in SANDBOXES:
    timezone = Site(
        client=site_info_session, site="sitegenesis", instance=sandbox,
    ).GetSiteInformation()
    if timezone.status_code == 200:
        siteinfo = timezone.json()
        print(f'{sandbox:60} {siteinfo["timezone"]}')
        if siteinfo["timezone"] != "Europe/London":
            print("Fixing timezone")
            fix_timezone(sandbox)
    else:
        print(sandbox, timezone)


for pig in PRODUCTION:
    timezone = Site(
        client=site_info_session, site="sitegenesis", instance=sandbox,
    ).GetSiteInformation()
    if timezone.status_code == 200:
        siteinfo = timezone.json()
        print(f'{sandbox:60} {siteinfo["timezone"]}')
    else:
        print(sandbox, timezone)
