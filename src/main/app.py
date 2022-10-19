import json
from datetime import datetime
import time
import os
from types import SimpleNamespace

from counterfit_connection import CounterFitConnection
from azure_iot.azure_device import IoTDevice
from azure_iot.azure_iot_hub import IoTHubClient
from azure_iot.azure_actuator import IoTActuator
from typing import Any


def initialise_hub(sensor_type: str, connection_str: str) -> IoTHubClient:
    return IoTHubClient(
        sensor_type,
        connection_str,
    )


def initialise_actuator(sensor: Any, iot_hub: IoTHubClient, pin: int) -> IoTActuator:
    iot_actuator = IoTActuator(
        sensor.actuator.type,
        sensor.actuator.value_triggered_at,
        pin,
        sensor.type,
        iot_hub,
    )
    iot_actuator.create_actuator()

    iot_actuator.configure_actuator()

    return iot_actuator


def initialise_device(
    sensor: Any,
    sensor_iot_hub: IoTHubClient,
    sensor_pin: int,
    iot_actuator: IoTActuator,
) -> IoTDevice:
    iot_device = IoTDevice(
        sensor.type,
        sensor.units,
        sensor.min,
        sensor.max,
        sensor.azure.device_id,
        sensor_iot_hub,
        iot_actuator,
    )

    iot_device.create_sensor(sensor_pin)

    iot_device.configure_sensor(sensor_pin)

    return iot_device


def run() -> None:
    iot_devices = []

    CounterFitConnection.init("127.0.0.1", 5000)

    conf_file = open("./config.json", "r")
    conf = json.load(conf_file, object_hook=lambda d: SimpleNamespace(**d))

    for i, sensor in enumerate(conf):
        sensor_conn_str_env_var = "{}_connection_str".format(sensor.azure.device_id)
        sensor_conn_str = os.getenv(sensor_conn_str_env_var)
        actuator_conn_str_env_var = "{}_connection_str".format(
            sensor.actuator.azure.device_id
        )
        actuator_conn_str = os.getenv(actuator_conn_str_env_var)

        if sensor_conn_str is None:
            raise Exception(
                "no connection string found with the name: " + sensor_conn_str_env_var
            )

        if actuator_conn_str is None:
            raise Exception(
                "no connection string found with the name: " + actuator_conn_str_env_var
            )

        sensor_hub = initialise_hub(sensor.type, sensor_conn_str)
        actuator_hub = initialise_hub(sensor.actuator.type, actuator_conn_str)
        actuator = initialise_actuator(sensor, actuator_hub, i + 20)
        sensor_device = initialise_device(sensor, sensor_hub, i, actuator)

        iot_devices.append(sensor_device)

    while True:
        time_now = datetime.now().isoformat()
        sensor_values = {time_now: []}

        for i, device in enumerate(iot_devices):
            sensor_value = device.read_sensor_values(i)
            sensor_values[time_now].append(sensor_value)

        sensor_hub.publish_message(sensor_values)
        sensor_value = None

        time.sleep(10)


if __name__ == "__main__":
    run()
