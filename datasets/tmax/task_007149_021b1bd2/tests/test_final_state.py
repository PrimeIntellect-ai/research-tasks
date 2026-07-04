# test_final_state.py

import os
import json
import pytest

def test_audit_summary_exists_and_correct():
    path = "/home/user/audit_summary.json"
    assert os.path.isfile(path), f"File {path} does not exist. You must create the JSON report."

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(data, dict), f"The JSON in {path} must be an object (dictionary)."

    expected_cwe = "CWE-78"
    actual_cwe = data.get("cwe_id")
    assert actual_cwe == expected_cwe, f"Expected 'cwe_id' to be '{expected_cwe}', but got '{actual_cwe}'."

    expected_cert = "server.crt"
    actual_cert = data.get("faulty_cert")
    assert actual_cert == expected_cert, f"Expected 'faulty_cert' to be '{expected_cert}', but got '{actual_cert}'."

    expected_line = 10
    actual_line = data.get("db_exposure_line")
    assert actual_line == expected_line, f"Expected 'db_exposure_line' to be {expected_line}, but got {actual_line}."