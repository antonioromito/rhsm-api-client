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


class SystemUUID:
    csv_columns = {
        'name': 'Name',
        'uuid': 'UUID',
        'type': 'type',
        'createdDate': 'Created Date',
        'createdBy': 'Created by',
        'lastCheckin': 'Last Check-In',
        'installedProductsCount': 'Installed Products',
        'entitlementsAttachedCount': 'Entitlement Count',
        'entitlementStatus': 'Entitlement Status',
        'complianceStatus': 'Compliance Status',
        'autoAttachSetting': 'Auto Attach Setting',
        'serviceLevelPreference': 'Service Level Preference',
        'factsCount': 'Facts',
        'errataApplicabilityCounts': 'Errata Counts'
    }

    def __init__(self, uuid, name, stype, created_date, created_by, last_checkin, installed_products_count,
                 entitlement_status, compliance_status, auto_attach_setting, service_level_preference,
                 facts_count, errata_applicability_counts, entitlements_attached_count):

        self.uuid = uuid
        self.name = name
        self.type = stype
        self.createdDate = created_date
        self.createdBy = created_by
        self.lastCheckin = last_checkin
        self.installedProductsCount = installed_products_count
        self.entitlementStatus = entitlement_status
        self.complianceStatus = compliance_status
        self.autoAttachSetting = auto_attach_setting
        self.serviceLevelPreference = service_level_preference
        self.factsCount = facts_count
        self.errataApplicabilityCounts = errata_applicability_counts
        self.entitlementsAttachedCount = entitlements_attached_count

        #self.securityCount = None
        #self.bugfixCount = None
        #self.enhancementCount = None

        #if self.errataApplicabilityCounts['valid'] is True:
        #    self.set_errata_counts()
        #elif self.errataApplicabilityCounts['valid'] is False:
        #    self.securityCount = 0
        #    self.bugfixCount = 0
        #    self.enhancementCount = 0

    #def set_errata_counts(self):
    #    self.securityCount = self.errataApplicabilityCounts['value']['securityCount']
    #    self.bugfixCount = self.errataApplicabilityCounts['value']['bugfixCount']
    #    self.enhancementCount = self.errataApplicabilityCounts['value']['enhancementCount']

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
        system = SystemUUID(uuid=data['uuid'], name=data['name'], stype=data['type'], created_date=data['createdDate'],
                            created_by=data['createdBy'], last_checkin=data['lastCheckin'],
                            installed_products_count=data['installedProductsCount'],
                            entitlement_status=data['entitlementStatus'], compliance_status=data['complianceStatus'],
                            auto_attach_setting=data['autoAttachSetting'],
                            service_level_preference=data['serviceLevelPreference'], facts_count=data['factsCount'],
                            errata_applicability_counts=data['errataApplicabilityCounts'],
                            entitlements_attached_count=data['entitlementsAttachedCount'])
        return system
