import json

class JSON:
  @staticmethod
  def write(data):
    print(json.dumps([d.serialize() for d in data]))
