from salesforce_ocapi.auth import CommerceCloudBMSession, EnvParser
import json
import httpx
from salesforce_ocapi.utils import csvopen

with EnvParser(path="examples/.env"):
    session = CommerceCloudBMSession()

INSTANCE = "https://production-eu01-example.demandware.net"
SITE = "sitegenesis"
IDList = csvopen("examples/databreach.csv")
for ID in IDList:
    url = f"{INSTANCE}/s/{sitegenesis}/dw/shop/v20_4/customers/{ID}"
    headers = {"Authorization": f"Bearer {session.RawToken}", "Content-Type": "application/json"}
    payload = {"enabled": False}
    response = httpx.patch(url, headers=headers, json=payload)

    r = response.json()
    # print(r)
    print(r["customer_id"], r["enabled"])

