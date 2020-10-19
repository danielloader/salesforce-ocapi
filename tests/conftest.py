import pytest
import respx
import json

BM_TOKEN = {
    "access_token": "2261e4b9-0550-4556-bf32-31706e419433",
    "expires_in": 899,
    "token_type": "Bearer",
}
CLIENT_TOKEN = {
    "access_token": "8GqCRI2hlL4tDb-V0xPLriQjLqs",
    "scope": "mail",
    "token_type": "Bearer",
    "expires_in": 1799,
}

CLIENT_ID = "11111111-2222-3333-4444-555555555555"
CLIENT_SECRET = "abcdefghijklmnopqrstuvwxyz"
BM_USER = "example@company.com"
BM_PASSWORD = "strongpassword"
OCAPI_VERSION = "v20_4"


@pytest.fixture(scope="session")
def mocked_instance_api():
    with respx.mock(base_url="https://test01-eu01-example.demandware.net") as respx_mock:
        respx_mock.post(
            f"/dw/oauth2/access_token?client_id={CLIENT_ID}", content=json.dumps(BM_TOKEN), alias="bmtokenrequest",
        )
        yield respx_mock


@pytest.fixture(scope="session")
def mocked_account_manager_api():
    with respx.mock(base_url="https://account.demandware.com") as respx_mock:
        respx_mock.post(
            "/dw/oauth2/access_token", content=json.dumps(CLIENT_TOKEN), alias="clienttokenrequest",
        )
        yield respx_mock

