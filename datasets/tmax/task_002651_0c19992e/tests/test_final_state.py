# test_final_state.py

import os
import json
import pytest

def test_imputed_data_json():
    output_path = '/home/user/imputed_data.json'

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Output path {output_path} is not a file."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    assert isinstance(data, list), f"JSON root must be a list, but got {type(data).__name__}."
    assert len(data) == 11, f"Expected 11 data points, but got {len(data)}."

    expected_y = [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0]

    mse = 0.0
    for i, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {i} is not a dictionary."
        assert 'time' in item, f"Item at index {i} is missing 'time' key."
        assert 'value' in item, f"Item at index {i} is missing 'value' key."

        time_val = item['time']
        value_val = item['value']

        assert isinstance(time_val, int), f"Time at index {i} must be an integer."
        assert isinstance(value_val, (int, float)), f"Value at index {i} must be a number."
        assert time_val == i, f"Expected time {i} at index {i}, but got {time_val}."

        mse += (value_val - expected_y[i]) ** 2

    mse /= len(data)

    threshold = 0.5
    assert mse <= threshold, f"MSE is {mse:.4f}, which exceeds the threshold of {threshold}."