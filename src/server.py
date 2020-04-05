from flask import Flask, jsonify, abort, make_response, request
from gevent.pywsgi import WSGIServer
import os 
import logging
import time

from log import initialize_logger
from data_handling import DataHandler
from database import Database

base_path = os.getcwd()
initialize_logger('{}/logs'.format(base_path))
app = Flask(__name__)

data_handler = DataHandler(base_path)


#TODO: Error handler


@app.route("/add/sensor-value", methods=["POST"])
def add_program():
    logging.debug("POST: add new program")
    if not request.json:
        make_response(jsonify({"error": "wrong request body"}), 400)

    data = request.json
    logging.debug("New data point: {}".format(data))
    data_stored = data_handler.add_data(data)
    
    if data_stored:
        return make_response(jsonify({"response": "OK"}), 200)
    else:
        return make_response(jsonify({"error": "internal error"}), 400)


@app.route("/values/humidity", methods=["GET"])
def get_humidity():
    values = data_handler.get_humidity()
    return make_response(jsonify(values), 200)


@app.route("/values/temperature", methods=["GET"])
def get_temperature():
    values = data_handler.get_temperature()
    return make_response(jsonify(values), 200)


@app.route("/values/moisture", methods=["GET"])
def get_moisture():
    values = data_handler.get_moisture()
    return make_response(jsonify(values), 200)


@app.route("/values/heat_index", methods=["GET"])
def get_heat_index():
    values = data_handler.get_heat_index()
    return make_response(jsonify(values), 200)


@app.route("/values/identifiers", methods=["GET"])
def get_value_identifiers():
    identifiers = ["humidity", "temperature", "moisture", "heat_index"]
    return make_response(jsonify(identifiers), 200)



@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


if __name__ == "__main__":
    logging.info("Starting server")
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
