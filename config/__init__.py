import json
import jsonschema


class Configuration:
    """
    Create a json file that will contain these fields
    spots -> list of number that indicate surf spot in MSW
    non_optional_hours -> list of hours that you can't surf in
    TOKEN -> string given by MSW API (a token)
    """
    def __init__(self, file_path):
        _obj = json.load(open(file_path, 'r'))
        conf_schema = {
            "type": "object",
            "properties": {
                "TOKEN": {"type": "string"},
                "SECRET_KEY": {"type": "string"},
                "non_optional_hours": {"type": "array"},
                "spots": {"type": "array"},
            }
        }
        jsonschema.validate(instance=_obj, schema=conf_schema)
        self.spots = _obj["spots"]
        self.token = _obj["TOKEN"]
        self.non_optional_hours = _obj["non_optional_hours"]

