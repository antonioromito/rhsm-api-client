import csv


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
