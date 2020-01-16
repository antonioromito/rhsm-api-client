from enum import Enum
from rhsm.formats.csv import CSV
from rhsm.formats.json import JSON
from rhsm.formats.json_pretty import JSON_Pretty

OUTPUT_FORMAT_DEFAULT = 'json_pretty'


class OutputFormat(Enum):
  JSON = 1
  JSON_PRETTY = 2
  CSV = 3

  @staticmethod
  def as_args():
    return [name.lower() for name, member in OutputFormat.__members__.items()]


class Outputter:
  def __init__(self, format, data):
    self.formatter = format
    if format == OutputFormat.JSON:
      self.formatter = JSON
    elif format == OutputFormat.JSON_PRETTY:
      self.formatter = JSON_Pretty
    elif format == OutputFormat.CSV:
      self.formatter = CSV
    self.data = data

  def write(self):
    formatted = self.formatter.write(self.data)
