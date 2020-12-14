"""Authentication classes, provide objects with renewable access tokens.
"""

import re
import time
from configparser import ConfigParser
from os import environ as env
from pathlib import Path

import httpx

from salesforce_ocapi.utils.exceptions import AuthenticationFailure, CredentialsMissing


class BaseToken:
    """Base object for shared attributes between different grant types
    """

    def __init__(
        self, client_id, client_secret, instance=None, bm_user=None, bm_password=None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bm_password = bm_password
        self.bm_user = bm_user
        self.instance = instance
        self.session = httpx.Client()

    def getToken(self):
        """Gets a token and stores it in the object, additionally injects an expiry time for renewing the token.
        """
        if self.bm_user and self.bm_password:
            url = f"{self.instance}/dw/oauth2/access_token?client_id={self.client_id}"
            payload = "grant_type=urn%3Ademandware%3Aparams%3Aoauth%3Agrant-type%3Aclient-id%3Adwsid%3Adwsecuretoken"
            auth = (self.bm_user, f"{self.bm_password}:{self.client_secret}")
        else:
            url = "https://account.demandware.com/dw/oauth2/access_token"
            payload = "grant_type=client_credentials"
            auth = (self.client_id, self.client_secret)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = self.session.post(url, headers=headers, data=payload, auth=auth,)
        token = response.json()
        try:
            assert response.status_code == 200
            assert "access_token" in token
            token.update({"expires_at": int(time.time()) + (token["expires_in"] - 15)})
        except AssertionError:
            authencation_errors = ["unauthorized_client", "invalid_client"]
            if "error" in token:
                if token["error"] in authencation_errors:
                    print(response.json())
                    raise AuthenticationFailure

        self.token = token

    def CheckExpiry(self):
        """Check token expiry and renew if needed.
        """
        if self.token["expires_at"] < int(time.time()):
            self.getToken()

    @property
    def AuthHeader(self) -> dict:
        """Returns a header value for an "Authorization" request header.

        Returns:
            dict: Formatted Bearer token string for use as a header.
        """
        self.CheckExpiry()
        return {"Authorization": f'Bearer {self.token["access_token"]}'}

    @property
    def RawToken(self):
        """Returns the value of the access_token key in the bearer token.

        Returns:
            str: Bearer token.
        """
        self.CheckExpiry()
        return self.token["access_token"]

    @property
    def Token(self):
        """Method to return a token in JSON.

        Returns:
            dict: Dictionary representation of the JSON bearer token response.
        """
        self.CheckExpiry()
        return self.token


class CommerceCloudClientSession(BaseToken):
    """Commerce Cloud Client Credentials Session

    All the arguments are optional, but only if you provide the values as an environmental variable:
        client_id is OCAPI_CLIENT_ID
        client_secret is OCAPI_CLIENT_SECRET
        instance is OCAPI_INSTANCE

    Args:
        client_id (str, optional): Client ID for OCAPI roles/authentication.
        client_seTypeErrorcret (str, optional): Client Secret for OCAPI roles/authentication.
        instance (str, optional): Top level domain of the SFCC instance.
            Optional since Client Credentials tokens can be used across multiple instances.
            Defaults to None.
    """

    def __init__(self, *, client_id=None, client_secret=None, instance=None, **kwargs):

        try:
            self.client_id = client_id or env["OCAPI_CLIENT_ID"]
            self.client_secret = client_secret or env["OCAPI_CLIENT_SECRET"]
            self.instance = instance or env["OCAPI_INSTANCE"]
        except KeyError:
            raise CredentialsMissing
        super().__init__(self.client_id, self.client_secret, self.instance)
        self.getToken()


class CommerceCloudBMSession(BaseToken):
    """Commerce Cloud Business Manager Session

    All the arguments are optional, but only if you provide the values as an environmental variable:
        client_id is OCAPI_CLIENT_ID
        client_secret is OCAPI_CLIENT_SECRET
        instance is OCAPI_INSTANCE
        bm_user is OCAPI_USERNAME
        bm_password is OCAPI_PASSWORD


    Args:
        client_id (str, optional): Client ID for OCAPI roles/authentication.
        client_secret (str, optional): Client Secret for OCAPI roles/authentication.
        instance (str, optional): Top level domain of the SFCC instance.
        bm_user (str, optional): Business Manager username, either local or SSO.
        bm_password (str, optional): Business Manager password.
    """

    def __init__(
        self,
        *,
        client_id=None,
        client_secret=None,
        instance=None,
        bm_user=None,
        bm_password=None,
        **kwargs,
    ):
        try:
            self.client_id = client_id or env["OCAPI_CLIENT_ID"]
            self.client_secret = client_secret or env["OCAPI_CLIENT_SECRET"]
            self.instance = instance or env["OCAPI_INSTANCE"]
            self.bm_user = bm_user or env["OCAPI_USERNAME"]
            self.bm_password = bm_password or env["OCAPI_PASSWORD"]
        except KeyError:
            raise CredentialsMissing
        super().__init__(
            self.client_id,
            self.client_secret,
            self.instance,
            self.bm_user,
            self.bm_password,
        )
        self.getToken()


class Profile:
    """Helper class for loading a profile file.

    Args:
        path (str, optional): Path to credentials file. Defaults to "~/.sfcc/credentials").
    """

    def __init__(
        self, path: str = Path.joinpath(Path.home(), Path(".sfcc/credentials"))
    ):
        self.path = path

    def read(self, profile: str = "default") -> dict:
        """Read credentials file.

        Reads the file and returns a dictionary for the profile key value pairs.

        Args:
            profile (str, optional): Credentials file section name. Defaults to "default".

        Returns:
            dict: Key value pairs for authentication.
        """
        parser = ConfigParser()
        parser.read(self.path)
        config = {**dict(parser.items("default")), **dict(parser.items(profile))}
        return config


class EnvParser:
    def __init__(self, path: str = ".env"):
        """.env file parser.

        Reads file for environmental variables.

        Args:
            path (str, optional): Path to .env file to load. Defaults to ".env".
        """
        envre = re.compile(r"""^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$""")
        self.envs = {}
        with open(Path(path)) as ins:
            for line in ins:
                match = envre.match(line)
                if match is not None:
                    self.envs[match.group(1)] = match.group(2)

    def __enter__(self):
        """Load dictionary into environmental variables."""
        for key, value in self.envs.items():
            env[key] = value

    def __exit__(self, type, value, traceback):
        """Unload environmental variables from dictionary keys."""
        for key in self.envs.keys():
            del env[key]
