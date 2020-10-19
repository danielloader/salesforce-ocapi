from salesforce_ocapi.auth import CommerceCloudBMSession
from ..conftest import CLIENT_ID, CLIENT_SECRET, BM_USER, BM_PASSWORD, BM_TOKEN
from httpx._client import Client as httpx_client


def get_mock_bm_session(mocked_instance_api):
    session = CommerceCloudBMSession(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        instance="https://test01-eu01-example.demandware.net",
        bm_user=BM_USER,
        bm_password=BM_PASSWORD,
    )
    return session


def test_token(mocked_instance_api):
    session = get_mock_bm_session(mocked_instance_api)
    assert hasattr(session, "getToken")
    assert hasattr(session, "CheckExpiry")
    assert session.Token["access_token"] == BM_TOKEN["access_token"]
    assert session.Token["expires_in"] == BM_TOKEN["expires_in"]
    assert session.Token["token_type"] == BM_TOKEN["token_type"]
    assert type(session.Token.get("expires_at")) is int
    assert type(session.session) is httpx_client


def test_rawtoken(mocked_instance_api):
    session = get_mock_bm_session(mocked_instance_api)
    assert type(session.RawToken) is str
    assert session.RawToken == BM_TOKEN["access_token"]


def test_authheader(mocked_instance_api):
    session = get_mock_bm_session(mocked_instance_api)
    assert type(session.AuthHeader) is dict
    assert session.AuthHeader == {"Authorization": f'Bearer {BM_TOKEN["access_token"]}'}
