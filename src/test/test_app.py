from dataclasses import dataclass
import pytest
from types import SimpleNamespace
from typing import Any, List

import mock
from src.main.app import initialise_actuator, initialise_device, initialise_hub
from src.main.azure_iot.azure_actuator import IoTActuator
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
                IoTHubClient(
                    device_name="Soil Moisture", connection_str="myconnectionstring"
                ),
                1,
                IoTActuator(
                    type="testType",
                    value_triggered_at=10,
                    pin=10,
                    sensor_type="testSensorType",
                    client=IoTHubClient(
                        device_name="Soil Moisture", connection_str="myconnectionstring"
                    ),
                ),
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
                actuator=IoTActuator(
                    type="testType",
                    value_triggered_at=10,
                    pin=10,
                    sensor_type="testSensorType",
                    client=IoTHubClient(
                        device_name="Soil Moisture", connection_str="myconnectionstring"
                    ),
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
                IoTHubClient(
                    device_name="Soil Moisture", connection_str="myconnectionstring"
                ),
                1,
                IoTActuator(
                    type="testType",
                    value_triggered_at=10,
                    pin=10,
                    sensor_type="testSensorType",
                    client=IoTHubClient(
                        device_name="Soil Moisture", connection_str="myconnectionstring"
                    ),
                ),
            ],
            want=None,
            raises_exception=True,
            exception_info="not all sensor details have been provided",
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


@mock.patch("src.main.azure_iot.azure_device.IoTDevice.create_sensor")
@mock.patch("src.main.azure_iot.azure_device.IoTDevice.configure_sensor")
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch(
    "src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client",
)
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_initialise_hub(
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
        want: IoTHubClient
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="intialises hub",
            args=["Soil Moisture", "myconnectionstring"],
            want=IoTHubClient(
                device_name="Soil Moisture", connection_str="myconnectionstring"
            ),
            raises_exception=False,
            exception_info="",
        ),
        TestCase(
            name="handles case when no sensor_type is provided",
            args=["", "something"],
            want=IoTHubClient(
                device_name="Soil Moisture", connection_str="myconnectionstring"
            ),
            raises_exception=True,
            exception_info="sensor_type cannot be empty",
        ),
        TestCase(
            name="handles case when no connection_str is provided",
            args=["something", ""],
            want=IoTHubClient(
                device_name="Soil Moisture", connection_str="myconnectionstring"
            ),
            raises_exception=True,
            exception_info="connection_str cannot be empty",
        ),
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                initialise_hub(*test_case.args)
            assert test_case.exception_info in str(e_info.value)
        else:
            got = initialise_hub(*test_case.args)
            assert got == test_case.want


@mock.patch("src.main.azure_iot.azure_actuator.IoTActuator.create_actuator")
@mock.patch("src.main.azure_iot.azure_actuator.IoTActuator.configure_actuator")
@mock.patch("src.main.azure_iot.azure_iot_hub.ADC")
@mock.patch(
    "src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client",
)
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_initialise_actuator(
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
        want: IoTActuator
        raises_exception: bool
        exception_info: str

    test_cases = [
        TestCase(
            name="initialises actuator",
            args=[
                SimpleNamespace(
                    type="Soil Moisture",
                    units="NoUnits",
                    min=0,
                    max=1023,
                    azure=SimpleNamespace(device_id="soil_moisture_sensor"),
                    actuator=SimpleNamespace(type="LED", value_triggered_at=10),
                ),
                IoTHubClient(
                    device_name="Soil Moisture", connection_str="myconnectionstring"
                ),
                1,
            ],
            want=IoTActuator(
                type="LED",
                value_triggered_at=10,
                pin=1,
                sensor_type="Soil Moisture",
                client=IoTHubClient(
                    device_name="Soil Moisture", connection_str="myconnectionstring"
                ),
            ),
            raises_exception=False,
            exception_info="",
        ),
        TestCase(
            name="handles case when not all details have been provided to actuator",
            args=[
                None,
                None,
                None,
            ],
            want=None,
            raises_exception=True,
            exception_info="not all actuator details have been provided",
        ),
    ]

    for test_case in test_cases:
        if test_case.raises_exception:
            with pytest.raises(Exception) as e_info:
                initialise_actuator(*test_case.args)
            assert test_case.exception_info in str(e_info.value)
        else:
            got = initialise_actuator(*test_case.args)
            assert got.pin == test_case.want.pin
