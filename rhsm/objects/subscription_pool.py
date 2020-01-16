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


class SubscriptionPool:
    def __init__(self, consumed, _id, quantity, _type):
        self.consumed = consumed
        self.id = _id
        self.quantity = quantity
        self.type = _type

    def serialize(self):
        return self.__dict__

    @staticmethod
    def deserialize(data):
        logging.debug('Deserializing from: %s', data)
        pool = SubscriptionPool(data['consumed'], data['id'], data['quantity'], data['type'])
        return pool
