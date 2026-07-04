# test_final_state.py
import os
import json
import math

def test_report_json_exists():
    """Verify that the report.json file was created."""
    assert os.path.isfile('/home/user/report.json'), "The file /home/user/report.json does not exist."

def test_report_json_content():
    """Verify the contents of report.json match the expected schema and values."""
    with open('/home/user/report.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/report.json is not a valid JSON file."

    # Check keys
    expected_keys = {"ks_statistic", "p_value", "is_equivalent"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, found {set(data.keys())}."

    # Check types
    assert isinstance(data["ks_statistic"], (int, float)), "ks_statistic must be a float."
    assert isinstance(data["p_value"], (int, float)), "p_value must be a float."
    assert isinstance(data["is_equivalent"], bool), "is_equivalent must be a boolean."

    # Check values
    assert math.isclose(data["ks_statistic"], 0.14, abs_tol=0.001), \
        f"Expected ks_statistic to be approx 0.1400, got {data['ks_statistic']}."

    assert math.isclose(data["p_value"], 0.7166, abs_tol=0.001), \
        f"Expected p_value to be approx 0.7166, got {data['p_value']}."

    assert data["is_equivalent"] is True, \
        f"Expected is_equivalent to be True, got {data['is_equivalent']}."

def test_script_exists():
    """Verify that the student's script exists."""
    assert os.path.isfile('/home/user/verify_results.py'), "The script /home/user/verify_results.py does not exist."