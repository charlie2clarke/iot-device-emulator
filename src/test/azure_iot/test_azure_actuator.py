from dataclasses import dataclass
from typing import Any, List

import mock
import pytest
from src.main.azure_iot.azure_actuator import IoTActuator
from src.main.azure_iot.azure_iot_hub import IoTHubClient


@pytest.mark.happy
@mock.patch("src.main.azure_iot.azure_device.IoTHubClient.post", return_value=200)
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_create_actuator(
    mock_post, mock_adc, mock_create_device_client, mock_iot_hub_device_client
):
    @dataclass
    class TestCase:
        name: str
        actuator: IoTActuator
        want: bool
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="actuator gets created successfully",
            actuator=IoTActuator(
                type="LED",
                value_triggered_at=10,
                pin=1,
                sensor_type="Soil Moisture",
                client=IoTHubClient(
                    device_name="testName",
                    connection_str="myconnectionstring",
                    counterfit_base_url="127.0.0.1",
                ),
            ),
            want=True,
            raises_exception=False,
            exception_info="",
        )
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                test_case.actuator.create_actuator()
            assert test_case.exception_info in str(e_info.value)
        else:
            got = test_case.actuator.create_actuator()
            assert got == test_case.want


@pytest.mark.happy
@mock.patch("src.main.azure_iot.azure_device.IoTHubClient.post", return_value=200)
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_configure_sensor(
    mock_post, mock_adc, mock_create_device_client, mock_iot_hub_device_client
):
    @dataclass
    class TestCase:
        name: str
        actuator: IoTActuator
        want: bool
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="actuator gets configured successfully",
            actuator=IoTActuator(
                type="LED",
                value_triggered_at=10,
                pin=1,
                sensor_type="Soil Moisture",
                client=IoTHubClient(
                    device_name="testName",
                    connection_str="myconnectionstring",
                    counterfit_base_url="127.0.0.1",
                ),
            ),
            want=True,
            raises_exception=False,
            exception_info="",
        )
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                test_case.actuator.configure_actuator()
            assert test_case.exception_info in str(e_info.value)
        else:
            got = test_case.actuator.configure_actuator()
            assert got == test_case.want
