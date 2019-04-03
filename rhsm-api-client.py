#!/usr/bin/env python2
#
# rhsm-api_client.py
#
# Copyright (C) 2019 Antonio Romito
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Please refer to the following bugzilla for more info:
# <https://bugzilla.redhat.com/show_bug.cgi?id=1597355>
#
# usage: rhsm-api-client.py [-h] -u USERNAME -p PASSWORD -c CLIENT_ID -s
#                               CLIENT_SECRET
#                               {systems,allocations,subscriptions,erratas,packages}
#                               ...
#
# RHSM API implementation
#
# positional arguments:
#   {systems,allocations,subscriptions,erratas,packages}
#                         Program mode: systems, allocations, subscriptions,
#                         errata, packages)
#     systems             Generate systems CSV report.
#     allocations         Generate allocations CSV report.
#     subscriptions       Generate subscriptions CSV report.
#     erratas             Generate erratas CSV report.
#     packages            Generate packages CSV report.
#
# optional arguments:
#   -h, --help            show this help message and exit
#
# authentication:
#   -u USERNAME, --username USERNAME
#                         Red Hat customer portal username
#   -p PASSWORD, --password PASSWORD
#                         Red Hat customer portal password
#   -c CLIENT_ID, --client_id CLIENT_ID
#                         Red Hat customer portal API Key Client ID
#   -s CLIENT_SECRET, --client_secret CLIENT_SECRET
#                         Red Hat customer portal API Key Client Secret
#
import requests
import csv
import argparse
import time
import sys
import os
from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session


class Systems:
    def __init__(self, pagination, body):
        self.pagination = pagination
        self.body = body

    def get_body(self):
        return self.body

    def get_count(self):
        return self.pagination['count']

    def get_limit(self):
        return self.pagination['limit']

    def get_offset(self):
        return self.pagination['offset']


class System:
    def __init__(self, entitlement_count, entitlement_status, errata_counts, href, last_checkin, name, stype, uuid):
        self.entitlementCount = entitlement_count
        self.entitlementStatus = entitlement_status
        self.errataCounts = errata_counts
        self.href = href
        self.lastCheckin = last_checkin
        self.name = name
        self.type = stype
        self.uuid = uuid

        self.securityCount = None
        self.bugfixCount = None
        self.enhancementCount = None

        if self.errataCounts is not None:
            self.set_errata_counts()
        else:
            self.securityCount = 0
            self.bugfixCount = 0
            self.enhancementCount = 0

    def set_errata_counts(self):
        self.securityCount = self.errataCounts['securityCount']
        self.bugfixCount = self.errataCounts['bugfixCount']
        self.enhancementCount = self.errataCounts['enhancementCount']

    def print_system_to_csv(self, csv_filename):
        with open(csv_filename, 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow([self.name, self.uuid, self.enhancementCount, self.type, "Not Available",
                                 self.entitlementStatus, self.lastCheckin, self.securityCount, self.bugfixCount,
                                 self.enhancementCount])

    def __repr__(self):
        return ('Name: %s UUID: %s Subscriptions Attached: %d Type: %s Cloud Provider: %s Status: %s '
                'Last Check in: %s Security Advisories: %d Bug Fixes: %d Enhancements: %d' %
                (self.name, self.uuid, self.enhancementCount, self.type, "Not Available", self.entitlementStatus,
                 self.lastCheckin, self.securityCount, self.bugfixCount, self.enhancementCount))


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


class Portal:
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
            print(time.ctime() + ' - The Round Trip Time (RTT) for %s is %.4fs. Status code is: %s' %
                  (response.url, (t2 - t1), response.status_code))

            try:
                response.raise_for_status()
                success = True
            except requests.exceptions.HTTPError:
                wait = 5
                retries += 1
                time.sleep(wait)
                print(time.ctime() + ' - Response status code code indicate a failed attempt to retrive data. '
                                     'Waiting %s secs and re-trying... Attempt number [%d]' % (str(wait), retries))

            if response.status_code == requests.codes.ok:
                return response.json()
            elif response.status_code != requests.codes.ok and retries == 3:
                sys.exit(time.ctime() + ' - Exiting after %d failed attempts to retrive data from: %s' % (retries,
                                                                                                          response.url))

    def systems(self, limit, offset):
        payload = {'limit': limit, 'offset': offset}
        json_output = self._get("systems", params=payload)
        return json_output


def output_file_check(csv_filename):
    if os.path.isfile(csv_filename):
        if is_python_3():
            text = input('CSV output file already exits. Do you want to override it? (y/N)')
        else:
            text = raw_input('CSV output file already exits. Do you want to override it? (y/N)')
        if text == "" or text.lower() == "n":
            sys.exit(time.ctime() + ' - Please change output filename path if you don\'t want to override existing '
                                    'file %s.' % csv_filename)
        elif text.lower() == "y":
            with open(csv_filename, 'w') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=',')
                csv_writer.writerow(['Name','UUID', 'Subscriptions Attached', 'Type', 'Cloud Provider', 'Status',
                                    'Last Check in', 'Security Advisories', 'Bug Fixes', 'Enhancements'])


def add_systems_command_options(subparsers):
    systems_parser = subparsers.add_parser('systems',
                                         help='Generate systems CSV report.')

    systems_parser.add_argument("-o", "--output_csv", help="Output CSV file", required=True)

    systems_parser.add_argument('-l', '--limit', help='The default and max number of result in a response are 100.',
                                default=100, required=False, action='store')


def add_allocations_command_options(subparsers):
    allocations_parser = subparsers.add_parser('allocations',
                                         help='Generate allocations CSV report.')


def add_subscriptions_command_options(subparsers):
    subscriptions_parser = subparsers.add_parser('subscriptions',
                                         help='Generate subscriptions CSV report.')


def add_erratas_command_options(subparsers):
    erratas_parser = subparsers.add_parser('erratas',
                                         help='Generate erratas CSV report.')

def add_packages_command_options(subparsers):
    systems_parser = subparsers.add_parser('packages',
                                         help='Generate packages CSV report.')


def run_systems(args):

    output_file_check(args.output_csv)

    total_count = 0
    all_systems = list()

    auth = AuthorizationCode(args.username, args.password, args.client_id, args.client_secret)
    auth.fetch_token()
    portal = Portal(auth)

    limit = int(args.limit)
    if limit > 100:
        limit = 100
        
    offset = 0
    while True:
        this_systems_json = portal.systems(limit, offset)
        this_systems = Systems(this_systems_json['pagination'], this_systems_json['body'])
        if this_systems.get_count() != 0:
            total_count = total_count + this_systems.get_count()
            offset = offset + limit
            for system in this_systems.get_body():
                if 'errataCounts' not in system:
                    system['errataCounts'] = None
                if 'lastCheckin' not in system:
                    system['lastCheckin'] = None

                this_system = System(system['entitlementCount'], system['entitlementStatus'], system['errataCounts'],
                                     system['href'], system['lastCheckin'], system['name'], system['type'],
                                     system['uuid'])

                this_system.print_system_to_csv(args.output_csv)
                all_systems.append(this_system)
        else:
            break

    print(time.ctime() + " - Total Number of systems in list: %d" % len(all_systems))
    print(time.ctime() + " - Total Number of systems from count: %d" % total_count)


def run_allocations(args):
    print('To be implemented')


def run_subscriptions(args):
    print('To be implemented')


def run_erratas(args):
    print('To be implemented')


def run_packages(args):
    print('To be implemented')


def is_python_3():
    if sys.version_info > (3, 0):
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description="RHSM API implementation")
    group = parser.add_argument_group('authentication')
    group.add_argument("-u", "--username", help="Red Hat customer portal username", required=True, action="store")
    group.add_argument("-p", "--password", help="Red Hat customer portal password", required=True, action="store")
    group.add_argument("-c", "--client_id", help="Red Hat customer portal API Key Client ID", required=True,
                       action="store")
    group.add_argument("-s", "--client_secret", help="Red Hat customer portal API Key Client Secret",
                       required=True, action="store")

    subparsers = parser.add_subparsers(help='Program mode: systems, allocations, subscriptions, errata, packages)',
                                       dest='mode')

    add_systems_command_options(subparsers)
    add_allocations_command_options(subparsers)
    add_subscriptions_command_options(subparsers)
    add_erratas_command_options(subparsers)
    add_packages_command_options(subparsers)

    args = parser.parse_args()

    if args.mode == "systems":
        run_systems(args)
    elif args.mode == "allocations":
        run_allocations(args)
    elif args.mode == "subscriptions":
        run_subscriptions(args)
    elif args.mode == "erratas":
        run_erratas(args)
    elif args.mode == "packages":
        run_packages(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
