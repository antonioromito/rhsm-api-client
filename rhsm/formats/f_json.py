import json


class JSON:
    @staticmethod
    def write(data):
        if isinstance(data, list):
            print(json.dumps([d.serialize() for d in data]))
        else:
            print(json.dumps(data.serialize()))
