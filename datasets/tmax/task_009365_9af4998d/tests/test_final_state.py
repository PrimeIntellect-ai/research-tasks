# test_final_state.py

import os
import json
import pytest

def test_process_script_exists():
    assert os.path.isfile('/home/user/process.py'), "The script /home/user/process.py does not exist."

def test_output_json_exists():
    assert os.path.isfile('/home/user/sensor_summary.json'), "The output file /home/user/sensor_summary.json does not exist. Did you run your script?"

def test_output_json_content():
    json_path = '/home/user/sensor_summary.json'
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    # Check keys
    for sensor in ["sensor_1", "sensor_2", "sensor_3"]:
        assert sensor in data, f"Key '{sensor}' is missing from the output JSON."
        assert isinstance(data[sensor], list), f"Value for '{sensor}' should be a list."
        assert len(data[sensor]) == 3, f"Expected 3 readings for '{sensor}', got {len(data[sensor])}."

    # Check sensor_1
    s1 = data["sensor_1"]
    assert s1[0]["timestamp"] == 3 and s1[0]["sma"] == 22.0, "Incorrect values for sensor_1 at timestamp 3."
    assert s1[1]["timestamp"] == 4 and s1[1]["sma"] == 24.0, "Incorrect values for sensor_1 at timestamp 4."
    assert s1[2]["timestamp"] == 5 and s1[2]["sma"] == 26.0, "Incorrect values for sensor_1 at timestamp 5."

    # Check sensor_2
    s2 = data["sensor_2"]
    assert s2[0]["timestamp"] == 3 and s2[0]["sma"] == 15.0, "Incorrect values for sensor_2 at timestamp 3."
    assert s2[1]["timestamp"] == 4 and s2[1]["sma"] == 20.0, "Incorrect values for sensor_2 at timestamp 4."
    assert s2[2]["timestamp"] == 5 and s2[2]["sma"] == 23.33, "Incorrect values for sensor_2 at timestamp 5."

    # Check sensor_3
    s3 = data["sensor_3"]
    assert s3[0]["timestamp"] == 3 and s3[0]["sma"] == 30.0, "Incorrect values for sensor_3 at timestamp 3."
    assert s3[1]["timestamp"] == 4 and s3[1]["sma"] == 30.0, "Incorrect values for sensor_3 at timestamp 4."
    assert s3[2]["timestamp"] == 5 and s3[2]["sma"] == 30.0, "Incorrect values for sensor_3 at timestamp 5."