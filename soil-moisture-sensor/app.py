import os
from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

os.environ['CONNECTION_STRING'] = 'HostName=ECM3440-Assignment.azure-devices.net;DeviceId=soil-moisture-sensor;SharedAccessKey=LQugzEuDImMNBT1olepKTWAa3GfxX50In00+tFAYcOI='
adc = ADC()
relay = GroveRelay(5)

device_client = IoTHubDeviceClient.create_from_connection_string(os.getenv('CONNECTION_STRING'))

print('Connecting')
device_client.connect()
print('Connected')

def handle_method_request(request):
    print("Direct method received - ", request.name)
    
    if request.name == "relay_on":
        relay.on()
    elif request.name == "relay_off":
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)

device_client.on_method_request_received = handle_method_request

while True:
    soil_moisture = adc.read(0)
    temperature = adc.read(1)
    humidity = adc.read(2)
    led1 = GroveLed(3)

    print("Soil moisture:", soil_moisture)
    print("Temperature:", temperature)
    print("Humidity:", humidity)

    message = Message(json.dumps({ 'soil_moisture': soil_moisture }))
    device_client.send_message(message)
    message = Message(json.dumps({ 'temperature': temperature }))
    device_client.send_message(message)
    message = Message(json.dumps({ 'humidity': humidity }))
    device_client.send_message(message)

    print('Turning LED on')
    led1.on()

    time.sleep(10)

    print('Turning LED off')
    led1.off()
    