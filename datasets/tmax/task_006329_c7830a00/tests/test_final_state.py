# test_final_state.py

import os
import re
import pytest

def test_sensor_data_generated():
    data_path = '/home/user/sensor_service/sensor_data.csv'
    assert os.path.isfile(data_path), f"{data_path} was not generated."
    assert os.path.getsize(data_path) > 0, f"{data_path} is empty."

def test_final_metrics_generated():
    metrics_path = '/home/user/sensor_service/final_metrics.txt'
    assert os.path.isfile(metrics_path), f"{metrics_path} was not generated."

def test_variance_calculation_accuracy():
    metrics_path = '/home/user/sensor_service/final_metrics.txt'
    assert os.path.isfile(metrics_path), f"{metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        content = f.read().strip()

    match = re.search(r'Variance:\s*([0-9\.]+)', content)
    assert match is not None, f"Format incorrect in {metrics_path}. Expected 'Variance: <value>'."

    variance = float(match.group(1))

    # The variance of Uniform(-1, 1) is 1/3 (~0.3333). 
    # With seed 42 and 100,000 samples, it should be approximately 0.3335.
    # The naive algorithm with catastrophic cancellation yields exactly 0.0 or a wildly incorrect value.
    assert 0.3300 <= variance <= 0.3400, (
        f"Variance {variance} is out of the expected numerical stability range (approx 0.3333). "
        "Catastrophic cancellation might not be fully fixed."
    )