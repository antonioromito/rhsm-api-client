# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/antonioromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import logging

logging.getLogger(__name__)


class Allocation:
    csv_columns = {
        'name': 'Name',
        'type': 'Type',
        'entitlementCount': 'Entitlement Count',
        'uuid': 'UUID',
        'version': 'Version',
        'url': 'URL',
    }

    def __init__(self, entitlement_count, name, _type, url, uuid, version):
        self.entitlementCount = entitlement_count
        self.name = name
        self.type = _type
        self.url = url
        self.uuid = uuid
        self.version = version

    def serialize(self):
        return self.__dict__

    @staticmethod
    def deserialize(data):
        allocation = Allocation(data['entitlementQuantity'], data['name'], data['type'],
                                data['url'], data['uuid'], data['version'])

        return allocation
