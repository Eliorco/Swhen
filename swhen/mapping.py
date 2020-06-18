class Mapping:
    mapper = { "3662": "Bat Yam",
                "3658": "Hilton TLV",
                "3663": "Hof Ma'aravi"
               }

    def __init__(self):
        pass

    def get_city(self, spot_code):
        return self.mapper.get(spot_code, None)

    def get_code(self, spot_name):
        for k,v in self.mapper.items():
            if v == spot_name:
                return k

        return None
