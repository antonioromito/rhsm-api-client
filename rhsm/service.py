# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/aromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.
import logging
import requests
import time
import sys
from oauthlib.oauth2 import TokenExpiredError, Client
from requests_oauthlib import OAuth2Session
from rhsm.objects.allocation import Allocation
from rhsm.objects.errata import Errata
from rhsm.objects.subscription import Subscription
from rhsm.objects.system import System
from rhsm.objects.system_uuid import SystemUUID
from rhsm.objects.image import Image

logging.getLogger(__name__)


class RHSMAuthorizationCode(object):
    TOKEN_PATH = ''

    def __init__(self, token_url, client_id, offline_token, token=None):
        self.token_url = token_url
        self.client_id = client_id
        self.offline_token = offline_token
        self.token = token

        self.session = OAuth2Session(client=Client(client_id=self.client_id,
                                                   refresh_token=self.offline_token))

    def refresh_token(self):
        self.token = self.session.refresh_token(token_url=self.token_url, client_id=self.client_id)
        return self.token


class RHSMApi(object):
    API_URL = 'https://api.access.redhat.com/management/v1'
    FETCH_LIMIT = 100

    def __init__(self, auth=None):
        self.auth = auth

    def _get(self, endpoint, params=None , stream=False):
        retries = 0
        success = False
        while not success and retries < 3:
            url = self.API_URL + '/' + endpoint
            logging.debug(time.ctime() + ' - Starting request: %s with params: %s ' % (url, params))
            if self.auth:
                # TO DO:
                # Implement the response.elapsed properties that returns a timedelta object with
                # the time elapsed from sending the request to the arrival of the response.
                #
                try:
                    t1 = time.time()
                    response = self.auth.session.get(url, params=params, stream=stream)
                    t2 = time.time()
                except TokenExpiredError:
                    logging.debug(time.ctime() + ' - Token has expired. Refreshing token...')
                    self.auth.refresh_token()
                    t1 = time.time()
                    response = self.auth.session.get(url, params=params, stream=stream)
                    t2 = time.time()
            else:
                t1 = time.time()
                response = requests.get(url, params=params, stream=stream)
                t2 = time.time()
            logging.debug(time.ctime() + (' - The Round Trip Time (RTT) for %s is %.4fs. '
                                          'Status code is: %s') %
                          (response.url, (t2 - t1), response.status_code))

            try:
                response.raise_for_status()
                success = True
            except requests.exceptions.HTTPError:
                wait = 5
                retries += 1
                time.sleep(wait)
                logging.debug(time.ctime() + ' - Response status code code indicate a failed attempt to '
                                     'retrive data. Waiting %s secs and re-trying... Attempt '
                                     'number [%d]' % (str(wait), retries))

            if response.status_code == requests.codes.ok:
                # HERE WE NEED TO INTERCEPT 307 REDIRECT AND ITS JSON RESPONSE (CASE OF DOWNLOAD ISO)
                #
                # if response.history:
                #    before_redirect = response.history
                #
                if response.headers['content-type'] == 'application/json':
                    return response.json()
                elif response.headers['content-type'] == 'application/octet-stream':
                    return response
                else:
                    sys.exit(time.ctime() + ' - Unmanaged Content-Type')

            elif response.status_code != requests.codes.ok and retries == 3:
                sys.exit(time.ctime() + ' - Exiting after %d failed attempts to retrive data from: '
                                        '%s' % (retries, response.url))

    def json_batch_fetch(self, fetch_func, deserialize_func):
        batch_set = []
        offset = 0
        while True:
            batch = fetch_func(offset)
            batch_count = batch['pagination']['count']
            logging.debug('Fetched %s more entries', batch_count)
            offset += self.FETCH_LIMIT
            for raw in batch['body']:
                logging.debug('Processing %s: %s', type(raw), raw)
                obj = deserialize_func(raw)
                batch_set.append(obj)
            if batch_count < self.FETCH_LIMIT:
                break
        return batch_set

    def json_single_fetch(self, fetch_func, deserialize_func):
        single = fetch_func
        obj = deserialize_func(single['body'])
        return obj

    def systems(self, uuid=None, include=None):
        if uuid is None:
            fetch_func = self.fetch_systems
            deserialize_func = System.deserialize
            batch = self.json_batch_fetch(fetch_func, deserialize_func)
            logging.debug('data is %s', fetch_func)
            return batch
        elif uuid and include is None:
            fetch_func = self.fetch_systems(offset=None, uuid=uuid)
            deserialize_func = SystemUUID.deserialize
            logging.debug("Deserialize :" + str(deserialize_func))
            single = self.json_single_fetch(fetch_func, deserialize_func)
            logging.debug('data is %s', fetch_func)
            return single
        elif uuid and include:
            fetch_func = self.fetch_systems(offset=None, uuid=uuid, include=include)
            deserialize_func = SystemUUID.deserialize
            single = self.json_single_fetch(fetch_func, deserialize_func)
            logging.debug('data is %s', fetch_func)
            return single

    def fetch_systems(self, offset, uuid=None, include=None):
        if uuid is None:
            payload = {'limit': self.FETCH_LIMIT, 'offset': offset}
            data = self._get("systems", params=payload)
        elif uuid and include is None:
            data = self._get("systems/" + uuid)
        elif uuid and include:
            payload = {'include': include}
            data = self._get("systems/" + uuid, params=payload)
        return data

    def allocations(self):
        fetch_func = self.fetch_allocations
        deserialize_func = Allocation.deserialize
        batch = self.json_batch_fetch(fetch_func, deserialize_func)
        return batch

    def fetch_allocations(self, offset):
        payload = {'limit': self.FETCH_LIMIT, 'offset': offset}
        data = self._get("allocations", params=payload)
        return data

    def errata(self):
        fetch_func = self.fetch_errata
        deserialize_func = Errata.deserialize
        batch = self.json_batch_fetch(fetch_func, deserialize_func)
        return batch

    def fetch_errata(self, offset):
        payload = {'limit': self.FETCH_LIMIT, 'offset': offset}
        data = self._get("errata", params=payload)
        return data

    def subscriptions(self):
        fetch_func = self.fetch_subscription
        deserialize_func = Subscription.deserialize
        batch = self.json_batch_fetch(fetch_func, deserialize_func)
        return batch

    def fetch_subscription(self, offset):
        payload = {'limit': self.FETCH_LIMIT, 'offset': offset}
        data = self._get("subscriptions", params=payload)
        return data

    def images(self, checksum=None):
        if checksum:
            fetch_func = self.fetch_images(checksum=checksum)
            deserialize_func = Image.deserialize
            image = self.json_single_fetch(fetch_func['response_json'], deserialize_func)
            image.write_to_file(fetch_func['response_data'], image.get_filename(checksum))

    def fetch_images(self, checksum):
        response = self._get("images/" + checksum + "/download", stream=True)
        data = {'response_json': None, 'response_data': None}
        # Getting JSON file info from 307 redirect
        #
        if response.history[0] and response.history[0].headers['content-type'] == 'application/json':
            data['response_json'] = response.history[0].json()
        # ISO Data from get request
        #
        data['response_data'] = response
        return data
