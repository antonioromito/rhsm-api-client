import json


class JSON_Pretty:
    @staticmethod
    def write(data):
        if isinstance(data, list):
            print(json.dumps([d.serialize() for d in data], sort_keys=True, indent=2))
        else:
            print(json.dumps(data.serialize(), sort_keys=True, indent=2))
