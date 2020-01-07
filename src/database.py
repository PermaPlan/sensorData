import sqlite3
from enum import Enum
import logging
import threading
import json

class Database(object):

    def __init__(self, path):
        """Connection to database to persist the processing history
        
        Arguments:
            path {str} -- Path to the sqlite-database 
        """
        
        self.path = path + '/data.db'
        self.tables = {
            "sensor_data": {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "sensor_id": "INTEGER",
                "humidity": "REAL",
                "temperature": "REAL",
                "moisture": "INTEGER",
                "moisture_analog": "INTEGER",
                "heat_index": "REAL",
                "timestamp": "REAL",
                "data_point": "INTEGER",
                "max_data_point": "INTEGER"
            },
            "sensor_data_aggregated": {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "sensor_id": "INTEGER",
                "humidity": "REAL",
                "temperature": "REAL",
                "moisture": "INTEGER",
                "moisture_analog": "INTEGER",
                "heat_index": "REAL",
                "timestamp": "REAL"
            }
        }

        self._create_tables(self.tables)

        # cursor, conn = self._get_cursor()
        # cursor.execute("CREATE TABLE IF NOT EXISTS sensor_data (id INTEGER PRIMARY KEY AUTOINCREMENT, sensor_id INTEGER, humidity REAL, temperature REAL, moisture INTEGER, moisture_analog INTEGER, heat_index REAL, timestamp REAL);")

    def add_values(self, sensor_id, humidity, temperature, moisture, moisture_analog, heat_index, timestamp, data_point, max_data_point):
        cursor, conn = self._get_cursor()
        cursor.execute("INSERT INTO sensor_data (sensor_id, humidity, temperature, moisture, moisture_analog, heat_index, timestamp, data_point, max_data_point) VALUES (?,?,?,?,?,?,?,?,?)", (sensor_id, humidity, temperature, moisture, moisture_analog, heat_index, timestamp, data_point, max_data_point))
        conn.commit()

    def add_aggregated_values(self, sensor_id, humidity, temperature, moisture, moisture_analog, heat_index, timestamp):
        cursor, conn = self._get_cursor()
        cursor.execute("INSERT INTO sensor_data_aggregated (sensor_id, humidity, temperature, moisture, moisture_analog, heat_index, timestamp) VALUES (?,?,?,?,?,?,?)", (sensor_id, humidity, temperature, moisture, moisture_analog, heat_index, timestamp))
        conn.commit()

    def get_columns(self, columns):
        cursor, conn = self._get_cursor() 
        cursor.execute("SELECT {} FROM sensor_data".format(str.join(",", columns)))
        values = []
        for row in cursor.fetchall():
            values.append(row)
        
        return values

    def _create_tables(self, table_schemas):
        cursor, conn = self._get_cursor()
        for table in table_schemas:
            logging.debug("Creating table {}".format(table))

            query = self._build_table_description(table, table_schemas[table])
            cursor.execute(query)

    def _build_table_description(self, table_name, schema):
        columns = [key + " " + schema[key] for key in schema]
        columns = str.join(",", columns)

        return "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns)

    '''
    INSPIRATION
    def get_all_programs(self):
        cursor, conn = self._get_cursor() 
        cursor.execute("SELECT program FROM programs")
        programs = []
        for (program,) in cursor.fetchall():
            program = program.replace("'", "\"")
            programs.append(json.loads(program))
        
        return programs

    def update_program(self, id, program):
        cursor, conn = self._get_cursor()
        cursor.execute("UPDATE programs SET program=? WHERE program_id=?", (program, id))
        conn.commit()

    def delete_program(self, id):
        cursor, conn = self._get_cursor()
        cursor.execute("DELETE FROM programs WHERE program_id=?", (id,))
        conn.commit()

    def get_valves(self):
        cursor, conn = self._get_cursor() 
        cursor.execute("SELECT valve_id FROM valves")
        valves = []
        for (valve_id,) in cursor.fetchall():
            valves.append(valve_id)
        
        return valves
    '''

    def _get_cursor(self):
        try:
            conn = sqlite3.connect(self.path)
            logging.info("Connected to database under {}".format(self.path))
            return conn.cursor(), conn
        except:
            logging.error("Could not establish connection to database under {}".format(self.path))