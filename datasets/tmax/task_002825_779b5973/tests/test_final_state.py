# test_final_state.py

import os
import json
import pytest

INTEGRITY_LOG_PATH = "/home/user/integrity.log"
REDACTED_REPORTS_PATH = "/home/user/redacted_reports.json"

def test_integrity_log():
    assert os.path.exists(INTEGRITY_LOG_PATH), f"{INTEGRITY_LOG_PATH} does not exist."
    with open(INTEGRITY_LOG_PATH, "r") as f:
        content = f.read().strip()
    assert content == "VALID", f"Expected 'VALID' in {INTEGRITY_LOG_PATH}, but found '{content}'."

def test_redacted_reports():
    assert os.path.exists(REDACTED_REPORTS_PATH), f"{REDACTED_REPORTS_PATH} does not exist."

    with open(REDACTED_REPORTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REDACTED_REPORTS_PATH} does not contain valid JSON.")

    expected_data = {
        "reports": [
            {"id": 1, "data": "Routine server maintenance completed.", "author": "alice"},
            {"id": 2, "data": "User [REDACTED] reported a billing error.", "author": "bob"},
            {"id": 3, "data": "Contractor [REDACTED] requires access to db-prod.", "author": "charlie"}
        ]
    }

    assert data == expected_data, "The redacted reports JSON does not match the expected structure and content."