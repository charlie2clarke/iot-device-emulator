from counterfit_shims_grove.grove_led import GroveLed

from .azure_iot_hub import IoTHubClient


class IoTActuator:
    ALLOWED_ACTUATORS = ["LED", "Relay"]

    def __init__(
        self,
        type: str,
        value_triggered_at: int,
        pin: int,
        sensor_type: str,
        client: IoTHubClient,
    ) -> None:
        self.type = type
        self.value_triggered_at = value_triggered_at
        self.pin = pin
        self.sensor_type = sensor_type
        self.client = client

        if self.type == "LED":
            self.led = GroveLed(self.pin)

    def create_actuator(self) -> bool:
        if self.type not in IoTActuator.ALLOWED_ACTUATORS:
            raise Exception("actuator is not valid")

        payload = {"type": self.type, "port": self.pin}

        http_code = self.client.post("/create_actuator", payload)
        if http_code != 200:
            raise Exception(
                "unsuccessful request to counterfit with payload: " + str(payload)
            )
        return True

    def configure_actuator(self) -> bool:
        payload = {"port": str(self.pin), "color": "#ff0000"}

        http_code = self.client.post("/led_actuator_settings", payload)
        if http_code != 200:
            raise Exception(
                "unsuccessful request to counterfit with payload: " + str(payload)
            )
        return True
