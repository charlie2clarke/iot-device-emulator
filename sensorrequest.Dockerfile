FROM python:3.8-slim-buster

ARG soil_moisture_sensor_connection_str
ARG temperature_sensor_connection_str
ARG humidity_sensor_connection_str
ARG soil_moisture_led_connection_str 
ARG temperature_led_connection_str
ARG humidity_led_connection_str

ENV soil_moisture_sensor_connection_str=${soil_moisture_sensor_connection_str}
ENV temperature_sensor_connection_str=${temperature_sensor_connection_str}
ENV humidity_sensor_connection_str=${humidity_sensor_connection_str}
ENV soil_moisture_led_connection_str=${soil_moisture_led_connection_str}
ENV temperature_led_connection_str=${temperature_sensor_connection_str}
ENV humidity_led_connection_str=${humidity_led_connection_str}

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "python3" , "src/main/app.py", "--counterfit", "counterfit"]
