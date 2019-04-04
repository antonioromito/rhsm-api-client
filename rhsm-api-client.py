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
import csv
import argparse
import time
import sys
import os
import systems
import rhsmapi
import rhauth


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

    authorization = rhauth.AuthorizationCode(args.username, args.password, args.client_id, args.client_secret)
    authorization.fetch_token()
    api_service = rhsmapi.RHSMapi(authorization)

    limit = int(args.limit)
    if limit > 100:
        limit = 100

    offset = 0
    while True:
        this_systems_json = api_service.systems(limit, offset)
        this_systems = systems.Systems(this_systems_json['pagination'], this_systems_json['body'])
        if this_systems.get_count() != 0:
            total_count = total_count + this_systems.get_count()
            offset = offset + limit
            for system in this_systems.get_body():
                if 'errataCounts' not in system:
                    system['errataCounts'] = None
                if 'lastCheckin' not in system:
                    system['lastCheckin'] = None

                this_system = systems.System(system['entitlementCount'], system['entitlementStatus'], system['errataCounts'],
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
