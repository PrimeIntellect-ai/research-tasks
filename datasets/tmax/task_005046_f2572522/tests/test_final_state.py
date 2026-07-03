# test_final_state.py
import os
import json
import pytest
import math

SUMMARY_FILE = '/home/user/summary.json'
PROCESS_SCRIPT = '/home/user/process.py'

def test_summary_file_exists():
    assert os.path.isfile(SUMMARY_FILE), f"The output file {SUMMARY_FILE} does not exist."

def test_summary_json_content():
    with open(SUMMARY_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {SUMMARY_FILE} does not contain valid JSON.")

    expected_data = {
        "S01": {"max_temperature": 37.0, "mean_vibration": 14.60, "temp_spikes": 3},
        "S02": {"max_temperature": 30.0, "mean_vibration": 9.50, "temp_spikes": 4},
        "S03": {"max_temperature": 50.0, "mean_vibration": 5.50, "temp_spikes": 4}
    }

    for sensor, expected_features in expected_data.items():
        assert sensor in data, f"Sensor {sensor} is missing from the summary JSON."
        actual_features = data[sensor]

        for feature, expected_val in expected_features.items():
            assert feature in actual_features, f"Feature '{feature}' is missing for sensor {sensor}."
            actual_val = actual_features[feature]

            if isinstance(expected_val, float):
                assert math.isclose(actual_val, expected_val, rel_tol=1e-2), \
                    f"Expected {feature} for {sensor} to be {expected_val}, but got {actual_val}."
            else:
                assert actual_val == expected_val, \
                    f"Expected {feature} for {sensor} to be {expected_val}, but got {actual_val}."

def test_parallel_processing_used():
    assert os.path.isfile(PROCESS_SCRIPT), f"The script {PROCESS_SCRIPT} does not exist."

    with open(PROCESS_SCRIPT, 'r') as f:
        script_content = f.read()

    has_multiprocessing = 'multiprocessing' in script_content or 'ProcessPoolExecutor' in script_content or 'concurrent.futures' in script_content
    assert has_multiprocessing, f"The script {PROCESS_SCRIPT} does not appear to use multiprocessing or concurrent.futures as required."