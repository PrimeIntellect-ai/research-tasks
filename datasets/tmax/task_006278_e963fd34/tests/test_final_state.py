# test_final_state.py
import os
import json

def test_vulnerabilities_log_exists():
    log_path = '/home/user/vulnerabilities.log'
    assert os.path.exists(log_path), f"The output file {log_path} does not exist."
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

def test_vulnerabilities_log_content():
    log_path = '/home/user/vulnerabilities.log'

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {log_path} does not contain valid JSON."

    expected_data = {
        "bin2": "audit_bypass_99",
        "bin4": "root_access_x"
    }

    assert isinstance(data, dict), "The JSON root must be an object (dictionary)."
    assert data == expected_data, (
        f"The contents of {log_path} do not match the expected output.\n"
        f"Expected: {expected_data}\n"
        f"Actual: {data}"
    )