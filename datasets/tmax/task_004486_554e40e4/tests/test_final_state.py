# test_final_state.py
import os
import json
import math
import pytest

OUTPUT_FILE = "/home/user/app/output.json"
DATA_DIR = "/home/user/app/data"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not generated. Did you run the pipeline?"

def test_output_contains_all_keys():
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{OUTPUT_FILE} is not a valid JSON file.")

    expected_keys = {f"sensor_{i}" for i in range(1, 7)}
    actual_keys = set(data.keys())

    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"Output JSON is missing expected keys: {missing_keys}"

def test_output_values_correct():
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check specific edge cases
    assert 'sensor_4' in data, "sensor_4 is missing from output"
    assert math.isclose(data['sensor_4'], 0.0, abs_tol=1e-9), f"sensor_4 activation should be 0.0, got {data['sensor_4']}"

    assert 'sensor_3' in data, "sensor_3 is missing from output"
    assert math.isclose(data['sensor_3'], 1.0, abs_tol=1e-9), f"sensor_3 activation should be 1.0, got {data['sensor_3']}"

    # Check standard cases
    assert 'sensor_5' in data, "sensor_5 is missing from output"
    assert math.isclose(data['sensor_5'], 0.5, abs_tol=1e-9), f"sensor_5 activation (input 0.0) should be 0.5, got {data['sensor_5']}"

def test_data_files_unmodified():
    # Ensure the original data files haven't been modified to "fix" the encoding issue
    data_1 = os.path.join(DATA_DIR, "data_1.json")
    data_2 = os.path.join(DATA_DIR, "data_2.json")

    assert os.path.isfile(data_1), "data_1.json is missing"
    assert os.path.isfile(data_2), "data_2.json is missing"

    # Check that data_2.json is still UTF-16
    try:
        with open(data_2, 'r', encoding='utf-16') as f:
            content = f.read()
            assert "sensor_3" in content
    except UnicodeDecodeError:
        pytest.fail("data_2.json was modified and is no longer valid UTF-16. You must fix the python script, not the data files.")