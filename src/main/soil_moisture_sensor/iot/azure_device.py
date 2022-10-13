import json
import time

from azure.iot.device import Message

from .azure_iot_hub import IoTHubClient


class IoTDevice:
    ALLOWED_SENSORS = ["Soil Moisture", "Temperature", "Humidity"]

    def __init__(
        self,
        type: str,
        units: str,
        min: int,
        max: int,
        device_id: str,
        client: IoTHubClient,
    ) -> None:
        self.type = type
        self.units = units
        self.min = min
        self.max = max
        self.device_id = device_id
        self.client = client

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.type == other.type
                and self.units == other.units
                and self.min == other.min
                and self.max == other.max
                and self.device_id == other.device_id
                and self.client == other.client
            )
        return False

    def create_sensor(self, i: int) -> None:
        if self.type not in IoTDevice.ALLOWED_SENSORS:
            raise Exception("sensor is not valid")

        payload = {
            "type": self.type,
            "pin": i,
            "i2c_pin": i,
            "port": "/dev/ttyAMA0",
            "name": "sensor_" + str(i),
            "unit": self.units,
            "i2c_unit": self.units,
        }

        http_code = self.client.post("/create_sensor", payload)
        if http_code != 200:
            raise Exception(
                "unsuccessful request to counterfit with payload: " + payload
            )

    def configure_sensor(self, i: int) -> None:
        if (self.min or self.max) is None:
            raise Exception("no min or max value set for sensor")

        payload = {
            "port": str(i),
            "value": i,
            "is_random": True,
            "random_min": self.min,
            "random_max": self.max,
        }

        http_code = self.client.post("/integer_sensor_settings", payload)
        if http_code != 200:
            raise Exception(
                "unsuccessful request to counterfit with payload: " + payload
            )

    def read_sensor_values(self, i, time):
        sensor_dict = {}

        sensor_name = "{}_{}".format(self.type, i)
        sensor_dict[sensor_name] = self.client.adc.read(i)

        print(sensor_name + " " + str(sensor_dict[sensor_name]))

        message = Message(
            json.dumps(
                {"name": self.type, "value": sensor_dict[sensor_name], "time": time}
            )
        )
        self.client.device_client.send_message(message)
