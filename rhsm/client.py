"""
Client interface that using Red Hat Subscription Manager (RHSM) APIs
to collect data from your account.
"""
# client.py
# gather information from RHSM and report it

# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/antonioromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.
import argparse
import logging
import time
import sys
import six
from rhsm.service import RHSMAuthorizationCode, RHSMApi
from rhsm.objects.system import System
from rhsm.outputter import Outputter, OutputFormat, OUTPUT_FORMAT_DEFAULT

logging.getLogger(__name__)

if six.PY3:
    raw_input = input


class RHSMClient(object):

    """The main rhsm-api-client class"""

    def __init__(self, parser):
        self._parser = parser
        self._args = self._parser.parse_args()
        self.mode = self._args.mode

    def get_service(self):
        authorization = RHSMAuthorizationCode(self._args.idp_token_url, self._args.client_id,
                                              self._args.token)
        authorization.refresh_token()
        api_service = RHSMApi(authorization)
        return api_service

    def output(self, batch):
        outformat = OutputFormat[self._args.format.upper()]
        outputter = Outputter(outformat, batch)
        outputter.write()

    def execute_systems(self):
        service = self.get_service()
        systems = None
        if self._args.uuid is None and self._args.include is None:
            systems = service.systems()
        elif self._args.uuid and self._args.include is None:
            systems = service.systems(uuid=self._args.uuid)
        elif self._args.uuid and self._args.include:
            systems = service.systems(uuid=self._args.uuid, include=self._args.include)
        logging.debug(systems)
        self.output(systems)

    def execute_allocations(self):
        service = self.get_service()
        all_allocations = service.allocations()
        self.output(all_allocations)

    def execute_subscriptions(self):
        service = self.get_service()
        all_subscriptions = service.subscriptions()
        self.output(all_subscriptions)

    def execute_errata(self):
        service = self.get_service()
        all_errata = service.errata()
        self.output(all_errata)

    def execute_packages(self):
        raise NotImplementedError


def add_systems_command_options(subparsers):
    systems_parser = subparsers.add_parser('systems', help='Fetch a list of systems.')

    systems_parser.add_argument('-u', '--uuid', help='The UUID of the system.', default=None, required=False,
                                action='store')

    systems_parser.add_argument("--include", help="Get details for a system specified by UUID.", default=None,
                                required=False, choices=['facts', 'entitlements', 'installedProducts'],
                                action='store')

    systems_parser.add_argument('-l', '--limit', help=('The default and max number of result in a '
                                                       'response are 100.'),
                                default=100, required=False, action='store')
    systems_parser.add_argument('-f', '--format', help='The format to output data as.',
                       choices=OutputFormat.as_args(), default=OUTPUT_FORMAT_DEFAULT)

def add_allocations_command_options(subparsers):
    subparsers.add_parser('allocations', help='Generate allocations CSV report.')


def add_subscriptions_command_options(subparsers):
    subparsers.add_parser('subscriptions', help='Generate subscriptions CSV report.')


def add_errata_command_options(subparsers):
    subparsers.add_parser('errata', help='Generate errata CSV report.')


def add_packages_command_options(subparsers):
    subparsers.add_parser('packages', help='Generate packages CSV report.')


def _get_parser():
    parser = argparse.ArgumentParser(description="RHSM API implementation")
    group = parser.add_argument_group('authentication')
    group.add_argument('-c', '--client_id', help=('Red Hat Customer Portal OIDC client '
                       "(default: %(default)s)"), action='store', default='rhsm-api')
    group.add_argument('-i', '--idp_token_url', help=('Red Hat Customer Portal SSO Token URL '
                       "(default: %(default)s)"), action='store',
                       default=('https://sso.redhat.com/auth/realms/redhat-external'
                                '/protocol/openid-connect/token'))
    group.add_argument('-t', '--token', help='Red Hat Customer Portal offline token',
                       required=True, action='store')


    subparsers = parser.add_subparsers(help=('Program mode: system, systems, allocations, subscriptions, '
                                       'errata, packages)'), dest='mode')

    add_systems_command_options(subparsers)
    add_allocations_command_options(subparsers)
    add_subscriptions_command_options(subparsers)
    add_errata_command_options(subparsers)
    add_packages_command_options(subparsers)

    return parser


def main():
    parser = _get_parser()
    rhsm = RHSMClient(parser)

    if rhsm.mode == "systems":
        rhsm.execute_systems()
    elif rhsm.mode == "allocations":
        rhsm.execute_allocations()
    elif rhsm.mode == "subscriptions":
        rhsm.execute_subscriptions()
    elif rhsm.mode == "errata":
        rhsm.execute_errata()
    elif rhsm.mode == "packages":
        rhsm.execute_packages()
