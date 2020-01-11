import time
import logging

from database import Database


class DataHandler(object):

    def __init__(self, path):
        self.data = {}
        self.max_data_point = 0
        self.db = Database(path)

    def add_data(self, data):
        if not data:
            return False
        print(data)
        humidity = data["air_humidity"]
        temperature = data["air_temperature"]
        moisture = data["soil_moisture"]
        moisture_analog = data["soil_moisture_analog"]
        heat_index = data["heat_index_C"]  
        timestamp = time.time()
        data_point = list(range(1, len(humidity)+1))
        data_point_max = len(humidity)

        for i in range(len(humidity)):

            self.db.add_values(
                #sensor_id="test", 
                humidity=humidity[i], 
                temperature=temperature[i],
                moisture=moisture[i],
                moisture_analog=moisture_analog[i],
                heat_index=heat_index[i],
                timestamp=time.time(),
                data_point= i,
                max_data_point= len(humidity)
            )

        data_point = data["data_point"]
        self.max_data_point = data["max_data_point"]
        self.data[data_point] = data

        logging.debug("Received data point {}/{}".format(data_point, self.max_data_point))

        if data_point == self.max_data_point - 1:
            self._aggregate_batch()

        return True

    def get_humidity(self):
        return self.get_data("humidity")

    def get_temperature(self):
        return self.get_data("temperature")

    def get_moisture(self):
        return self.get_data("moisture")

    def get_heat_index(self):
        return self.get_data("heat_index")

    def get_data(self, key):
        columns = ["timestamp", key]
        values = self.db.get_columns(columns)

        values_as_dict = [self._result_to_dict(row, columns) for row in values]
        return values_as_dict

    def _result_to_dict(self, result, columns):
        result_dict = {}
        for i, column in enumerate(columns):
            result_dict[column] = result[i]
        
        return result_dict

    def _aggregate_batch(self):
        logging.info("Aggregate collected batch")

        keys = [
            "air_humidity",
            "air_temperature",
            "soil_moisture",
            "soil_moisture_analog",
            "heat_index_C"
        ]
        aggregated = {key: 0 for key in keys}

        for data_point in self.data.values():
            for key in keys:
                aggregated[key] += data_point[key]

        for key in aggregated:
            aggregated[key] /= self.max_data_point

        self.db.add_aggregated_values(
            sensor_id="test", 
            humidity=aggregated["air_humidity"], 
            temperature=aggregated["air_temperature"], 
            moisture=aggregated["soil_moisture"], 
            moisture_analog=aggregated["soil_moisture_analog"],
            heat_index=aggregated["heat_index_C"],  
            timestamp=time.time()
        )

        self.data = {}
        self.max_data_point = 0
