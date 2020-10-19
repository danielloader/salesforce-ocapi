from salesforce_ocapi.auth import CommerceCloudClientSession
import requests

session = CommerceCloudClientSession(
    client_id="ADDCLIENTID",
    client_secret="ADDSECRET",
    instance="https://production-eu01-example.demandware.net",
)

categories = ["CHLBAKTEA", "BAKBRDBRN"]


def get_category_information(catalogid: str, categoryid: str):
    url = f"{session.instance}/s/-/dw/data/v20_4/catalogs/{catalogid}/categories/{categoryid}"
    headers = {"Authorization": session.AuthHeader()}
    response = requests.request("GET", url, headers=headers)
    if response.ok:
        return response.json()
    else:
        return response.status_code


for category in categories:
    print(get_category_information("master-catalog", category))
