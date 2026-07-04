# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The final report file {REPORT_PATH} is missing."

def test_report_content():
    assert os.path.isfile(REPORT_PATH), f"Cannot verify content because {REPORT_PATH} does not exist."

    try:
        with open(REPORT_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    expected_data = {
        "INFO": 2,
        "ERROR": 1,
        "CRITICAL": 1
    }

    assert data == expected_data, f"The aggregated counts in {REPORT_PATH} are incorrect. Expected {expected_data}, got {data}."