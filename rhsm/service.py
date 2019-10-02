# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/aromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.
import requests
import time
import sys
from oauthlib.oauth2 import TokenExpiredError, LegacyApplicationClient
from requests_oauthlib import OAuth2Session


class RHSMAuthorizationCode(object):
    TOKEN_URL = 'https://sso.redhat.com/auth/realms/3scale/protocol/openid-connect/token'

    def __init__(self, username, password, client_id, client_secret, token=None):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

        self.session = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))

    def fetch_token(self):
        self.token = self.session.fetch_token(
                token_url=self.TOKEN_URL, username=self.username, password=self.password,
                client_id=self.client_id, client_secret=self.client_secret)
        return self.token

    def refresh_token(self):
        self.token = self.session.refresh_token(token_url=self.TOKEN_URL, client_id=self.client_id,
                                                client_secret=self.client_secret)
        return self.token


class RHSMApi(object):
    API_URL = 'https://api.access.redhat.com/management/v1'

    def __init__(self, auth=None):
        self.auth = auth

    def _get(self, endpoint, params=None):
        retries = 0
        success = False
        while not success and retries < 3:
            url = self.API_URL + '/' + endpoint
            print(time.ctime() + ' - Starting request: %s with params: %s ' % (url, params))
            if self.auth:
                try:
                    t1 = time.time()
                    response = self.auth.session.get(url, params=params)
                    t2 = time.time()
                except TokenExpiredError:
                    print(time.ctime() + ' - Token has expired. Refreshing token...')
                    self.auth.refresh_token()
                    t1 = time.time()
                    response = self.auth.session.get(url, params=params)
                    t2 = time.time()
            else:
                t1 = time.time()
                response = requests.get(url, params=params)
                t2 = time.time()
            print(time.ctime() + (' - The Round Trip Time (RTT) for %s is %.4fs. '
                                  'Status code is: %s') %
                  (response.url, (t2 - t1), response.status_code))

            try:
                response.raise_for_status()
                success = True
            except requests.exceptions.HTTPError:
                wait = 5
                retries += 1
                time.sleep(wait)
                print(time.ctime() + ' - Response status code code indicate a failed attempt to '
                                     'retrive data. Waiting %s secs and re-trying... Attempt '
                                     'number [%d]' % (str(wait), retries))

            if response.status_code == requests.codes.ok:
                return response.json()
            elif response.status_code != requests.codes.ok and retries == 3:
                sys.exit(time.ctime() + ' - Exiting after %d failed attempts to retrive data from: '
                                        '%s' % (retries, response.url))

    def systems(self, limit, offset):
        payload = {'limit': limit, 'offset': offset}
        json_output = self._get("systems", params=payload)
        return json_output
