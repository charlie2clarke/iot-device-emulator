from app import create_sensor
import logging
import pytest


def test_create_sensor(mocker):
    test_cases = [
        {"name": "valid sensor is created", "input": [1, "Soil Mositure"], "want": True}
    ]
    for test_case in test_cases:
        logging.info(test_case["name"])
        something = mocker.patch("app._do_counterfit_req", return_value=200)
        something.assert_once_called()
        got = create_sensor(test_case["input"])
        assert got == test_case["want"]
