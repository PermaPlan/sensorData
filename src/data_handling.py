import time
import logging
from utils import median

from database import Database


class DataHandler(object):

    def __init__(self, path):
        self.data = {}
        self.max_data_point = 0
        self.db = Database(path)

    def add_data(self, data):
        logging.debug(data)
        if not data:
            return False

        humidity = data["air_humidity"]
        temperature = data["air_temperature"]
        moisture = data["soil_moisture"]
        moisture_analog = data["soil_moisture_analog"]
        heat_index = data["heat_index_C"]  
        timestamp = data["timestamp"]
        max_data_point = len(humidity)

        for i in range(len(humidity)):

            self.db.add_values(
                sensor_id="test", 
                humidity=humidity[i], 
                temperature=temperature[i],
                moisture=moisture[i],
                moisture_analog=moisture_analog[i],
                heat_index=heat_index[i],
                timestamp=timestamp,
                data_point=i,
                max_data_point=max_data_point 
            )

        humidity_median = median(humidity)
        temperature_median = median(temperature)
        moisture_median = median(moisture)
        moisture_analog_median = median(moisture_analog)
        heat_index_median = median(heat_index)

        self.db.add_aggregated_values(
            sensor_id="test", 
            humidity=humidity_median, 
            temperature=temperature_median, 
            moisture=moisture_median, 
            moisture_analog=moisture_analog_median,
            heat_index=heat_index_median,  
            timestamp=timestamp
        )

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
