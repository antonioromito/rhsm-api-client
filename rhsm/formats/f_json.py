import f_json


class JSON:
    @staticmethod
    def write(data):
        if isinstance(data, list):
            print(f_json.dumps([d.serialize() for d in data]))
        else:
            print(f_json.dumps(data.serialize()))
