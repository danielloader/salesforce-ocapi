from salesforce_ocapi.auth import CommerceCloudBMSession, EnvParser
from salesforce_ocapi.endpoints import Orders, CustomObjectsSearch
import json

with EnvParser(path="examples/.env"):
    session = CommerceCloudBMSession()

search_result = CustomObjectsSearch(client=session).SearchCustomObjects(
    object_type="OrderUpdate",
    body={
        "query": {
            "term_query": {
                "fields": ["c_orderUpdateFailed"],
                "operator": "is",
                "values": [True],
            }
        },
        "select": "(next, total, hits.(key_value_string))",
    },
)


ordernumbers = [
    (x["key_value_string"], x["key_value_string"].split("_")[0])
    for x in search_result.json()["hits"]
]
print(ordernumbers)

for order in ordernumbers:
    print(order)
    response = (
        Orders(client=session, site="sitegenesis")
        .PatchOrder(order=order[1], body={"c_pickedStatus": False})
        .json()
    )
    print(json.dumps(response))
    payment_id = response["payment_instruments"][0]["payment_instrument_id"]
    print(payment_id)
    response = Orders(client=session, site="sitegenesis").PatchPaymentIntrument(
        order=order[1],
        payment_instrument_id=payment_id,
        body={"payment_method_id": "PayPal", "c_isCaptureFailed": False},
    )
    print(response.text)
