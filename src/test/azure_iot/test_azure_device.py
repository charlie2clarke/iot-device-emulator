import mock
from http.server import HTTPServer
import pytest
from dataclasses import dataclass
from typing import List, Any

from src.main.azure_iot.azure_device import IoTDevice
from src.main.azure_iot.azure_iot_hub import IoTHubClient


@pytest.mark.happy
@mock.patch("src.main.azure_iot.azure_device.IoTHubClient.post", return_value=200)
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_create_sensor(
    mock_post, mock_adc, mock_create_device_client, mock_iot_hub_device_client
):
    @dataclass
    class TestCase:
        name: str
        device: IoTDevice
        args: List[Any]
        want: bool
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="sensor gets successfully created",
            device=IoTDevice(
                type="Soil Moisture",
                units="testUnits",
                min=1,
                max=2,
                device_id="testId",
                client=IoTHubClient(
                    device_name="testName", connection_str="testConnectionStr"
                ),
            ),
            args=[
                1,
            ],
            want=True,
            raises_exception=False,
            exception_info=None,
        ),
        TestCase(
            name="raises exception if sensor type is not allowd",
            device=IoTDevice(
                type="invalid type",
                units="testUnits",
                min=1,
                max=2,
                device_id="testId",
                client=IoTHubClient(
                    device_name="testName", connection_str="testConnectionStr"
                ),
            ),
            args=[1],
            want=None,
            raises_exception=True,
            exception_info="sensor is not valid",
        ),
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                test_case.device.create_sensor(*test_case.args)
            assert test_case.exception_info in str(e_info.value)
        else:
            got = test_case.device.create_sensor(*test_case.args)
            assert got == test_case.want


@pytest.mark.sad
@mock.patch("src.main.azure_iot.azure_device.IoTHubClient.post", return_value=500)
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_create_sensor(
    mock_post, mock_adc, mock_create_device_client, mock_iot_hub_device_client
):
    @dataclass
    class TestCase:
        name: str
        device: IoTDevice
        args: List[Any]
        want: bool
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="raises exception when counterfit fails",
            device=IoTDevice(
                type="Soil Moisture",
                units="testUnits",
                min=1,
                max=2,
                device_id="testId",
                client=IoTHubClient(
                    device_name="testName", connection_str="testConnectionStr"
                ),
            ),
            args=[1],
            want=None,
            raises_exception=True,
            exception_info="unsuccessful request to counterfit with payload:",
        ),
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                test_case.device.create_sensor(*test_case.args)
            assert test_case.exception_info in str(e_info.value)
        else:
            got = test_case.device.create_sensor(*test_case.args)
            assert got == test_case.want

def test_configure_sensor():
    
    pass