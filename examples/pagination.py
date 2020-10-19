from salesforce_ocapi.auth import CommerceCloudBMSession, Profile
from salesforce_ocapi.endpoints import (
    OrderSearch,
    ProductSearch,
)
from salesforce_ocapi.utils import Paginator


credentials = Profile().read("dev15")
session = CommerceCloudBMSession(**credentials)


# GET PAGINATION

paginator = Paginator(
    ProductSearch(client=session, site="sitegenesis"), "Search", progress=True
)

# All results in pages
for page in paginator.paginate(params={"q": "ham", "count": "200"}):
    print(page["hits"])

# Each hit as a yielded result
for hit in paginator.hits(params={"q": "ham", "count": "100"}):
    pass
    # paginator.write(hit["link"])


# JMESpath filter
for filtered_result in paginator.search(
    "hits[?contains(product_id, '76457') == `true`]",
    params={"q": "ham", "count": "200"},
):
    print(filtered_result)


# POST PAGINATION

paginator = Paginator(
    endpoint=OrderSearch(client=session, site="sitegenesis"),
    method="Search",
    progress=True,
    body={"select": "(**)", "query": {"match_all_query": {}}},
)

for order in paginator.hits(params={"count": 100}):
    paginator.write(order["data"]["order_no"])
