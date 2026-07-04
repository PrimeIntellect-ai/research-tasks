# test_final_state.py

import os
import json
import pytest

REPORT_FILE = "/home/user/anomaly_report.json"

def test_report_file_exists():
    assert os.path.exists(REPORT_FILE), f"The report file {REPORT_FILE} was not created."
    assert os.path.isfile(REPORT_FILE), f"{REPORT_FILE} is not a valid file."

def test_report_file_content():
    assert os.path.exists(REPORT_FILE), f"Cannot check content, {REPORT_FILE} missing."

    try:
        with open(REPORT_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_FILE} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {REPORT_FILE}: {e}")

    expected = {
        "data_01.zip": [1024, 4096],
        "data_03.zip": [2048],
        "data_05.zip": []
    }

    assert data == expected, (
        f"The contents of {REPORT_FILE} do not match the expected output.\n"
        f"Expected: {expected}\n"
        f"Got: {data}"
    )