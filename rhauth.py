from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session


class AuthorizationCode:
    TOKEN_URL = 'https://sso.redhat.com/auth/realms/3scale/protocol/openid-connect/token'

    def __init__(self, username, password, client_id, client_secret, token=None):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

        self.session = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))

    def fetch_token(self):
        self.token = self.session.fetch_token(token_url=self.TOKEN_URL, username=self.username, password=self.password,
                                              client_id=self.client_id, client_secret=self.client_secret)
        return self.token

    def refresh_token(self):
        self.token = self.session.refresh_token(token_url=self.TOKEN_URL, client_id=self.client_id,
                                                client_secret=self.client_secret)
        return self.token
