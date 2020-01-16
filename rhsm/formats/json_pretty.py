import json

class JSON_Pretty:
  @staticmethod
  def write(data):
    print(json.dumps([d.serialize() for d in data], sort_keys=True, indent=2))
