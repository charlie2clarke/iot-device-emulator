import json
import datetime
import os
import time
from types import SimpleNamespace

from counterfit_connection import CounterFitConnection
from .azure_iot.azure_device import IoTDevice
from .azure_iot.azure_iot_hub import IoTHubClient
from typing import Any


def initialise_device(sensor: Any, connection_str: str, i: int) -> IoTDevice:
    if sensor.type == "":
        if sensor.units == "":
            raise Exception("not all sensor details have been provided")

    if connection_str == "":
        raise Exception("connection_str cannot be empty")

    iot_hub = IoTHubClient(
        sensor.type,
        connection_str,
    )

    iot_device = IoTDevice(
        sensor.type,
        sensor.units,
        sensor.min,
        sensor.max,
        sensor.azure.device_id,
        iot_hub,
    )

    iot_device.create_sensor(i)

    iot_device.configure_sensor(i)

    return iot_device


def run() -> None:
    iot_devices = []

    CounterFitConnection.init("127.0.0.1", 5000)

    conf_file = open("./config.json", "r")
    conf = json.load(conf_file, object_hook=lambda d: SimpleNamespace(**d))

    for i, sensor in enumerate(conf):
        conn_str_env_var = "{}_connection_str".format(sensor.azure.device_id)
        connection_string = os.getenv(conn_str_env_var)

        if connection_string == "":
            raise Exception(
                "no connection string found with the name: " + conn_str_env_var
            )

        iot_device = initialise_device(sensor, connection_string, i)
        iot_devices.append(iot_device)

    while True:
        for i, device in enumerate(iot_devices):
            # passing in time so that each batch of sensor readings can be grouped to the nearest second.
            time = datetime.now()
            device.read_sensor_values(i, time)
        time.sleep(10)


if __name__ == "__main__":
    run()
