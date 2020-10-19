from salesforce_ocapi.auth import CommerceCloudClientSession
from ..conftest import CLIENT_ID, CLIENT_SECRET, CLIENT_TOKEN
from httpx._client import Client as httpx_client


def get_mock_client_session(mocked_account_manager_api):
    session = CommerceCloudClientSession(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, instance="https://test01-eu01-example.demandware.net",
    )
    return session


def test_token(mocked_account_manager_api):
    session = get_mock_client_session(mocked_account_manager_api)
    assert hasattr(session, "getToken")
    assert hasattr(session, "CheckExpiry")
    assert session.Token["access_token"] == CLIENT_TOKEN["access_token"]
    assert session.Token["expires_in"] == CLIENT_TOKEN["expires_in"]
    assert session.Token["token_type"] == CLIENT_TOKEN["token_type"]
    assert type(session.Token.get("expires_at")) is int
    assert type(session.session) is httpx_client


def test_rawtoken(mocked_account_manager_api):
    session = get_mock_client_session(mocked_account_manager_api)
    assert type(session.RawToken) is str
    assert session.RawToken == CLIENT_TOKEN["access_token"]


def test_authheader(mocked_account_manager_api):
    session = get_mock_client_session(mocked_account_manager_api)
    assert type(session.AuthHeader) is dict
    assert session.AuthHeader == {"Authorization": f'Bearer {CLIENT_TOKEN["access_token"]}'}
