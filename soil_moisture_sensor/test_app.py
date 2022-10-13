from app import add
from iot.azure_device import IoTDevice
from iot.azure_iot_hub import IoTHubClient


def test_add():
    assert add(2, 2) == 4


# def test_initialise_device():
#     test_cases = [
#         {
#             "name": "Initliases valid sensor",
#             "args": [
#                 {
#                     "type": "Soil Moisture",
#                     "units": "NoUnits",
#                     "min": 0,
#                     "max": 1023,
#                     "azure": {"device_id": "soil_moisture_sensor"},
#                 },
#                 "myconnectionstring",
#                 1,
#             ],
#             "want": IoTDevice(
#                 type="Soil Moisture",
#                 units="NoUnits",
#                 min=0,
#                 max=1023,
#                 device_id="soil_moisture_sensor",
#                 client=IoTHubClient(
#                     device_name="Soil Moisture", connection_str="myconnectionstring"
#                 ),
#             ),
#         }
#     ]

#     # mocker.patch("iot.azure_device.IoTDevice.create_sensor")
#     # mocker.patch("iot.azure_device.IoTDevice.configure_sensor")

#     for test_case in test_cases:
#         got = initialise_device(test_case["args"])
#         print("oiiiii")
#         assert got == test_case["want"]
