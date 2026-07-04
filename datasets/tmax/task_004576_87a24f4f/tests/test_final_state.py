# test_final_state.py

import os
import json
import pytest

def test_max_rolling_json_exists_and_correct():
    output_path = "/home/user/max_rolling.json"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did you run your script and save the output?"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    expected_data = {
        "1": 25,
        "3": 5,
        "4": 150
    }

    assert isinstance(data, dict), f"The JSON in {output_path} should be a dictionary mapping user IDs to integers."

    # Convert keys to strings if they are not already, though json.load does this automatically for dict keys.
    # However, we should ensure the values match exactly.
    assert data == expected_data, f"The content of {output_path} does not match the expected output. Expected {expected_data}, but got {data}."

def test_etl_script_exists():
    script_path = "/home/user/etl.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."