import csv
from functools import reduce
import sys

def getattrdeep(obj, attr):
  return reduce(getattr, attr.split('.'), obj)

class CSV:
  columns = {
    'name': 'Name',
    'uuid': 'UUID',
    'type': 'type',
    'entitlementCount': 'Entitlement Count',
    'entitlementStatus': 'Entitlement Status',
    'href': 'href',
    'lastCheckin': 'Last Check-In',
    'securityCount': 'Security Advisories',
    'bugfixCount': 'Bug Fixes',
    'enhancementCount': 'Enhancements',
  }

  @staticmethod
  def write(data):
    csv_writer = csv.writer(sys.stdout, delimiter=',')
    csv_writer.writerow(CSV.columns.values())
    for d in data:
      row = []
      for attr in CSV.columns.keys():
        row.append(getattrdeep(d, attr))
      csv_writer.writerow(row)
