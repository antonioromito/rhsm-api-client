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


class Errata:
    csv_columns = {
        'advisoryId': 'Advisory ID',
        'type': 'Type',
        'publishDate': 'Publish Date',
        'affectedSystemCount': 'Affected Systems',
        'synopsis': 'Synopsis',
    }

    def __init__(self, advisory_id, affected_system_count, details, publish_date,
                 synopsis, systems, _type):
        self.advisoryId = advisory_id
        self.affectedSystemCount = affected_system_count
        self.details = details
        self.publishDate = publish_date
        self.synopsis = synopsis
        self.systems = systems
        self.type = _type

    def serialize(self):
        return self.__dict__

    @staticmethod
    def deserialize(data):
        logging.debug('Deserializing from: %s', data)
        errata = Errata(data['advisoryId'], data['affectedSystemCount'], data['details'],
                        data['publishDate'], data['synopsis'], data['systems'], data['type'])
        return errata
