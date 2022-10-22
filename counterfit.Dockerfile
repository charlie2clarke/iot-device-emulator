FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install Counterfit

EXPOSE 5000

CMD [ "counterfit" ]
