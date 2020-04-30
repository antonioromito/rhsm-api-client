import csv
from functools import reduce
import sys


def getattrdeep(obj, attr):
    return reduce(getattr, attr.split('.'), obj)


class CSV:
    @staticmethod
    def write(data):
        if not data:
            return
        csv_writer = csv.writer(sys.stdout, delimiter=',', quoting=csv.QUOTE_ALL)
        if isinstance(data, list):
            csv_writer.writerow(data[0].csv_columns.values())
            for d in data:
                row = []
                for attr in d.csv_columns.keys():
                    row.append(getattrdeep(d, attr))
                csv_writer.writerow(row)
        else:
            csv_writer.writerow(data.csv_columns.values())
            row = []
            for attr in data.csv_columns.keys():
                row.append(getattrdeep(data, attr))
            csv_writer.writerow(row)
