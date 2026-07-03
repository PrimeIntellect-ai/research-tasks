# test_final_state.py

import os
import json
import math

def test_dq_check_script_exists():
    """Test that the python script was created."""
    script_path = "/home/user/dq_check.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_dq_metrics_json_exists():
    """Test that the output JSON file was created."""
    json_path = "/home/user/dq_metrics.json"
    assert os.path.exists(json_path), f"The output file {json_path} is missing."
    assert os.path.isfile(json_path), f"The path {json_path} is not a file."

def test_dq_metrics_json_content():
    """Test that the output JSON file contains the correct metrics."""
    json_path = "/home/user/dq_metrics.json"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {json_path} does not contain valid JSON."

    expected_keys = {"mean", "ci_lower", "ci_upper", "t_statistic", "p_value"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected keys. Found: {list(data.keys())}"

    expected_values = {
        "mean": 155.6793,
        "ci_lower": 153.0782,
        "ci_upper": 158.2104,
        "t_statistic": 4.1352,
        "p_value": 0.0000
    }

    for key, expected_val in expected_values.items():
        val = data[key]
        assert isinstance(val, (int, float)), f"Value for {key} should be a number, got {type(val)}."
        assert math.isclose(val, expected_val, abs_tol=1e-4), \
            f"Value for {key} is incorrect. Expected {expected_val}, got {val}."