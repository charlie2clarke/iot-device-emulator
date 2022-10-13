import os
import json
import requests
from azure.iot.device import IoTHubDeviceClient, MethodResponse
from counterfit_shims_grove.adc import ADC


class IoTHubClient:
    def __init__(
        self,
        device_name: str,
        connection_str: str,
    ) -> None:
        self.device_name = device_name
        self.adc = ADC()
        self.connection_str = connection_str
        try:
            self.device_client = self.create_device_client()
        except Exception as e:
            print("couldn't create device_client")
            print(e)
            os._exit(502)

        self.device_client.connect()
        self.device_client.on_method_request_received = self.set_request_handler

        print("connected to " + self.device_name)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.device_name == other.device_name
                and self.connection_str == other.connection_str
            )
        return False

    def set_request_handler(self, request):
        print("Direct method received - ", request.name)

        method_response = MethodResponse.create_from_method_request(request, 200)
        self.device_client.send_method_response(method_response)

    def create_device_client(self) -> IoTHubDeviceClient:
        return IoTHubDeviceClient.create_from_connection_string(self.connection_str)

    def post(self, endpoint, payload) -> int:
        url = "http://localhost:5000{}".format(endpoint)

        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)

        return response.status_code
