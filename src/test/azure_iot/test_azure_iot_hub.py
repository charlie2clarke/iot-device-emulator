from dataclasses import dataclass

import mock
import pytest
from pytest_httpserver import HTTPServer
from src.main.azure_iot.azure_iot_hub import IoTHubClient


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("127.0.0.1", 5000)


@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_post(
    mock_create_device_client, mock_iot_hub_device_client, httpserver: HTTPServer
):
    # check that the server is called with the correct request
    iot_hub_client = IoTHubClient(
        device_name="device name", connection_str="connection string"
    )

    httpserver.expect_request("/test").respond_with_data("yoo")

    code = iot_hub_client.post("/test", {"test": "testing testing, one two, one two"})

    assert code == 200
