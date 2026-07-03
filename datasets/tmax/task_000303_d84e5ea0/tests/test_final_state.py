# test_final_state.py

import os
import json
import pytest

def test_top_anomalies_json():
    json_path = '/home/user/top_anomalies.json'
    assert os.path.exists(json_path), f"Missing file: {json_path}. The script did not create the output JSON."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    # Ground truth derivation:
    # After dropping rows with 'ERR' (indices 3 and 8), we compute the rolling covariance (window=3)
    # between sensor_a and sensor_b, fill the first two with 0.0, and compute the score.
    # The top 3 scores correspond to these timestamps.
    expected = ["2023-01-01T05:00", "2023-01-01T04:00", "2023-01-01T07:00"]

    assert isinstance(data, list), f"Expected {json_path} to contain a list, got {type(data).__name__}."
    assert data == expected, f"The top anomalies list is incorrect. Expected {expected}, but got {data}."

def test_anomaly_plot_png():
    png_path = '/home/user/anomaly_plot.png'
    assert os.path.exists(png_path), f"Missing file: {png_path}. The script did not save the plot."

    with open(png_path, 'rb') as f:
        header = f.read(8)

    expected_magic = b'\x89PNG\r\n\x1a\n'
    assert header == expected_magic, f"The file {png_path} is not a valid PNG image. Ensure matplotlib saves correctly using a headless backend."