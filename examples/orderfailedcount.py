from salesforce_ocapi.auth import CommerceCloudBMSession, EnvParser
from salesforce_ocapi.endpoints import OrderSearch
import json
from collections import Counter

with EnvParser(path="examples/.env"):
    session = CommerceCloudBMSession()


search_result = OrderSearch(client=session, site="sitegenesis").Search(
    body={
        "query": {"match_all_query": {}},
        "select": "(hits.(data.(order_no, creation_date, customer_info, payment_instruments)))",
        "sorts": [{"field": "creation_date", "sort_order": "asc"}],
        "count": 10,
    }
)


# determine if there's any hits to this request
hits = search_result.json().get("hits")
if hits:
    # create list of customers from the orders found
    customers_with_failed_orders = dict(
        Counter([x["data"]["customer_info"]["customer_no"] for x in hits])
    )

    # create list of payment instruments in orders found
    payments = [x["data"].get("payment_instruments", {}) for x in hits]

    # flatten the payment instruments into the payment methods
    flatten = Counter(
        [
            x.get("payment_method_id")
            for x in [item for sublist in payments for item in sublist]
        ]
    )

    # count how many orders failed per customer id
    counted_occurances = {
        k: v
        for k, v in sorted(
            customers_with_failed_orders.items(), key=lambda item: item[1]
        )
    }

    # print resulting information
    print(
        json.dumps(
            {
                "total": len(hits),
                "dedupe_total": len(customers_with_failed_orders),
                "counts": counted_occurances,
                "payment_methods": flatten,
            },
            indent=2,
        )
    )
