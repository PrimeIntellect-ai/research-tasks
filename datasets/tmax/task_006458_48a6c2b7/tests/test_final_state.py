# test_final_state.py

import os
import json
import subprocess
import pytest

def test_extracted_payload_json():
    payload_path = "/home/user/extracted_payload.json"
    assert os.path.exists(payload_path), f"File {payload_path} does not exist."

    with open(payload_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {payload_path}: {e}")

    expected_data = {
        "service": "payment-api",
        "status": "down",
        "last_ping": 1700000000,
        "error": "OOM"
    }

    assert data == expected_data, f"Extracted payload JSON does not match expected data. Got: {data}"

def test_uptime_pytest_passes():
    test_file = "/home/user/test_uptime.py"
    assert os.path.exists(test_file), f"File {test_file} does not exist."

    res = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert res.returncode == 0, f"pytest on {test_file} failed with output:\n{res.stdout}\n{res.stderr}"