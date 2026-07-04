# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/rotation_report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Expected report file {REPORT_PATH} is missing."

def test_report_is_valid_json():
    with open(REPORT_PATH, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

def test_report_contents():
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)

    assert isinstance(data, dict), f"Expected JSON root to be a dictionary, got {type(data).__name__}."

    # Check keys
    expected_keys = {"cwe", "seed", "cert_cn"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Report is missing required keys: {', '.join(missing_keys)}"

    # Check CWE
    cwe = data.get("cwe")
    assert cwe in ["CWE-338", "CWE-327"], f"Expected 'cwe' to be 'CWE-338' or 'CWE-327', but got '{cwe}'."

    # Check seed
    seed = data.get("seed")
    assert seed == 13371337, f"Expected 'seed' to be 13371337, but got {seed}."

    # Check cert_cn
    cert_cn = data.get("cert_cn")
    assert cert_cn == "internal-service.local", f"Expected 'cert_cn' to be 'internal-service.local', but got '{cert_cn}'."