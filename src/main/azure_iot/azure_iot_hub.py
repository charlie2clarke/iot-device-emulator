import json
import logging
import os
from typing import Dict

import requests
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from counterfit_shims_grove.adc import ADC


class IoTHubClient:
    def __init__(
        self, device_name: str, connection_str: str, counterfit_base_url: str
    ) -> None:
        self.device_name = device_name
        self.adc = ADC()
        self.connection_str = connection_str
        self.counterfit_base_url = counterfit_base_url
        try:
            self.device_client = self.create_device_client()
        except Exception as e:
            logging.error("couldn't create device_client")
            logging.error(e)
            os._exit(502)

        self.device_client.connect()
        self.device_client.on_method_request_received = self.set_request_handler

        logging.info("connected to " + self.device_name)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.device_name == other.device_name
                and self.connection_str == other.connection_str
            )
        return False

    def set_request_handler(self, request):
        logging.info("Direct method received - ", request.name)

        method_response = MethodResponse.create_from_method_request(request, 200)
        self.device_client.send_method_response(method_response)

    def create_device_client(self) -> IoTHubDeviceClient:
        return IoTHubDeviceClient.create_from_connection_string(self.connection_str)

    def post(self, endpoint, payload) -> int:
        url = "http://{}:5000{}".format(self.counterfit_base_url, endpoint)

        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)

        return response.status_code

    def publish_message(self, msg: Dict) -> None:
        message = Message(json.dumps(msg))
        self.device_client.send_message(message)
