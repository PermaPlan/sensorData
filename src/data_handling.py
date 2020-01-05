import time

class DataHandler(object):

    def __init__(self):
        self.data = {}
        self.index = 0

    def add_data(self, data):
        if not data:
            return False

        ts = time.time()
        data["timestamp"] = ts

        self.data[self.index] = data
        self.index += 1

        return True

    def get_humidity(self):
        return self.get_data("humidity")

    def get_temperature(self):
        return self.get_data("temperature")

    def get_moisture(self):
        return self.get_data("moisture")

    def get_data(self, key):
        values = [{
            "timestamp": entry["timestamp"],
            "value": entry[key]
        } for entry in self.data.values()]

        return values

