import logging
from datetime import datetime

from .azure_actuator import IoTActuator
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
        actuator: IoTActuator,
    ) -> None:
        self.type = type
        self.units = units
        self.min = min
        self.max = max
        self.device_id = device_id
        self.client = client
        self.actuator = actuator

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

    def create_sensor(self, i: int) -> bool:
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
                "unsuccessful request to counterfit with payload: " + str(payload)
            )
        return True

    def configure_sensor(self, i: int) -> bool:
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
                "unsuccessful request to counterfit with payload: " + str(payload)
            )
        return True

    def read_sensor_values(self, i) -> dict:
        sensor_dict = {}

        sensor_name = "{}_{}".format(self.type, i)
        value = self.client.adc.read(i)

        if value <= self.actuator.value_triggered_at:
            logging.info("{} actuator trigger".format(str(self.actuator.sensor_type)))

            actuator_msg = {
                "name": self.actuator.type,
                "sensor_type": self.actuator.sensor_type,
                "time": datetime.now().isoformat(),
            }

            self.actuator.client.publish_message(actuator_msg)

        sensor_dict[sensor_name] = value

        logging.info(sensor_name + " " + str(sensor_dict[sensor_name]))

        return {
            "name": self.type,
            "value": sensor_dict[sensor_name],
        }
