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

logging.getLogger(__name__)


class System:
    def __init__(self, entitlement_count, entitlement_status, errata_counts, href, last_checkin,
                 name, stype, uuid):
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

    def get_keys(self):
        keys = [self.name, self.uuid, self.enhancementCount, self.type, "Not Available",
                self.entitlementStatus, self.lastCheckin, self.securityCount, self.bugfixCount,
                self.enhancementCount]
        return keys

    def __repr__(self):
        return ('Name: %s UUID: %s Subscriptions Attached: %d Type: %s Cloud Provider: %s '
                'Status: %s Last Check in: %s Security Advisories: %d Bug Fixes: %d '
                'Enhancements: %d' % (self.name, self.uuid, self.enhancementCount, self.type,
                                      "Not Available", self.entitlementStatus, self.lastCheckin,
                                      self.securityCount, self.bugfixCount, self.enhancementCount))

    def serialize(self):
        return self.__dict__

    @staticmethod
    def deserialize(data):
        if 'errataCounts' not in data:
            data['errataCounts'] = None
        if 'lastCheckin' not in data:
            data['lastCheckin'] = None

        system = System(data['entitlementCount'], data['entitlementStatus'],
                        data['errataCounts'], data['href'], data['lastCheckin'],
                        data['name'], data['type'], data['uuid'])

        return system
