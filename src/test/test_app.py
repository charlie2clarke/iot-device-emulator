from dataclasses import dataclass
import pytest
from types import SimpleNamespace
from typing import Any, List

import mock
from src.main.app import initialise_device
from src.main.azure_iot.azure_device import IoTDevice
from src.main.azure_iot.azure_iot_hub import IoTHubClient


@mock.patch("src.main.azure_iot.azure_device.IoTDevice.create_sensor")
@mock.patch("src.main.azure_iot.azure_device.IoTDevice.configure_sensor")
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch(
    "src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client",
)
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_initialise_device(
    mock_create_sensor,
    mock_configure_sensor,
    mock_adc,
    mock_create_device_client,
    mock_connect,
):
    @dataclass
    class TestCase:
        name: str
        args: List[Any]
        want: IoTDevice
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="Initialises valid sensor",
            args=[
                SimpleNamespace(
                    type="Soil Moisture",
                    units="NoUnits",
                    min=0,
                    max=1023,
                    azure=SimpleNamespace(device_id="soil_moisture_sensor"),
                ),
                "myconnectionstring",
                1,
            ],
            want=IoTDevice(
                type="Soil Moisture",
                units="NoUnits",
                min=0,
                max=1023,
                device_id="soil_moisture_sensor",
                client=IoTHubClient(
                    device_name="Soil Moisture", connection_str="myconnectionstring"
                ),
            ),
            raises_exception=False,
            exception_info="",
        ),
        TestCase(
            name="Handles case when not all sensor details have been provided",
            args=[
                SimpleNamespace(
                    type="",
                    units="",
                    min=0,
                    max=1023,
                    azure=SimpleNamespace(device_id="soil_moisture_sensor"),
                ),
                "myconnectionstring",
                1,
            ],
            want=None,
            raises_exception=True,
            exception_info="not all sensor details have been provided",
        ),
        TestCase(
            name="Handles case when an empty connection string is passed",
            args=[
                SimpleNamespace(
                    type="Type",
                    units="Units",
                    min=0,
                    max=1023,
                    azure=SimpleNamespace(device_id="soil_moisture_sensor"),
                ),
                "",
                1,
            ],
            want=None,
            raises_exception=True,
            exception_info="connection_str cannot be empty",
        ),
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                initialise_device(*test_case.args)
            assert test_case.exception_info in str(e_info.value)
        else:
            got = initialise_device(*test_case.args)
            assert got == test_case.want
