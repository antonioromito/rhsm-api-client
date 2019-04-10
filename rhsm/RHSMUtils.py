# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/aromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.
import os
import csv


class CSVReport(object):
    def __init__(self, filename):
        self.filename = filename

    def check_if_exists(self):
        if os.path.isfile(self.filename):
            return True

    def write_header(self, *args):
        _header = list(args)
        with open(self.filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(_header)

    def add_row(self, *args):
        _row = list(args)
        with open(self.filename, 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(_row)
