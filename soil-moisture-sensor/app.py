import json
import os
from types import SimpleNamespace

import requests
from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

import json
import time

from azure.iot.device import IoTHubDeviceClient, Message
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC

ALLOWED_SENSORS = [
    "Soil Moisture",
    "Temperature"
]

connection_string = os.getenv("IOT_CONNECTION_STRING")
if connection_string is None:
    raise Exception("IOT_CONNECTION_STRING is not set")

adc = ADC()

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')

def _do_counterfit_req(endpoint, payload):
    url = 'http://localhost:5000{}'.format(endpoint)

    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code


def create_sensor(i, sensor):
    if sensor.type not in ALLOWED_SENSORS:
        raise Exception("sensor is not valid")

    payload = {
        "type": sensor.type,
        "pin": i,
        "i2c_pin": i,
        "port": "/dev/ttyAMA0",
        "name": "sensor_" + str(i),
        "unit": sensor.units,
        "i2c_unit": sensor.units,
    }

    http_code = _do_counterfit_req("/create_sensor", payload)
    if http_code != 200:
        raise Exception("unsuccessful request to counterfit with payload: " + payload)


def configure_sensor(i, sensor):
    if (sensor.min or sensor.max) is None: 
        raise Exception("no min or max value set for sensor")

    payload = {
        "port": str(i),
        "value": i,
        "is_random": True,
        "random_min": sensor.min,
        "random_max": sensor.max
    }

    http_code = _do_counterfit_req("/integer_sensor_settings", payload)
    if http_code != 200:
        raise Exception("unsuccessful request to counterfit with payload: " + payload)


def read_sensor_values(sensors):
    sensor_dict = {}

    while True:
        for i in range(len(sensors)):
            sensor = sensors[i]
            sensor_name = '{}_{}'.format(sensor.type, i)
            sensor_dict[sensor_name] = adc.read(i)
            print(sensor_name + " " + str(sensor_dict[sensor_name]))

            json_sensor_name = sensor.type.lower().replace(" ", "_")

            message = Message(json.dumps({ json_sensor_name: sensor_dict[sensor_name] }))
            device_client.send_message(message)

        time.sleep(10)


if __name__ == "__main__":
    conf_file = open("./config.json", "r")
    conf = json.load(conf_file, object_hook=lambda d: SimpleNamespace(**d))

    for i, sensor in enumerate(conf):
        create_sensor(i, sensor)
        configure_sensor(i, sensor)

    read_sensor_values(conf)
    