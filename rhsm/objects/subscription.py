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
from rhsm.objects.subscription_pool import SubscriptionPool

logging.getLogger(__name__)


class Subscription:
    csv_columns = {
        'subscriptionName': 'Name',
        'subscriptionNumber': 'Subscription Number',
        'status': 'Status',
        'quantity': 'Quantity',
        'sku': 'SKU',
        'startDate': 'Start Date',
        'endDate': 'End Date',
        'poolCount': 'Pool Count',
        'contractNumber': 'Contract Number',
    }

    def __init__(self, contract_number, end_date, pools, quantity, sku, start_date,
                status, subscription_name, subscription_number):
        self.contractNumber = contract_number
        self.endDate = end_date
        self.pools = pools
        self.poolCount = len(self.pools)
        self.quantity = quantity
        self.sku = sku
        self.startDate = start_date
        self.status = status
        self.subscriptionName = subscription_name
        self.subscriptionNumber = subscription_number

    def serialize(self):
        attrs = [a for a in dir(self) if not a.startswith('_') and not callable(getattr(self, a))]
        s = {}
        for key in attrs:
            if key.startswith('_'):
                continue
            if key == 'pools':
                s[key] = [p.serialize() for p in self.pools]
            else:
                s[key] = getattr(self, key)
        return s

    @staticmethod
    def deserialize(data):
        if 'pools' not in data:
            data['pools'] = []

        if 'contractNumber' not in data:
            data['contractNumber'] = None

        pools = []
        for pool_raw in data['pools']:
            pool = SubscriptionPool.deserialize(pool_raw)
            pools.append(pool)

        subscription = Subscription(data['contractNumber'], data['endDate'], pools, data['quantity'],
                                    data['sku'], data['startDate'], data['status'],
                                    data['subscriptionName'], data['subscriptionNumber'])

        return subscription
