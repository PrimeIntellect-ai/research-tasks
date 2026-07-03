# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    """Test that the report.json file was created."""
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

def test_report_content():
    """Test that the report.json contains the correct aggregated data and missing indexes."""
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON")

    assert "total_users" in report, "Key 'total_users' missing from report"
    assert "total_orders" in report, "Key 'total_orders' missing from report"
    assert "missing_indexes" in report, "Key 'missing_indexes' missing from report"

    assert report["total_users"] == 5, f"Expected total_users to be 5, got {report['total_users']}"
    assert report["total_orders"] == 6, f"Expected total_orders to be 6, got {report['total_orders']}"

    expected_index = "CREATE INDEX idx_orders_user_id ON orders(user_id);"
    missing_indexes = report["missing_indexes"]

    assert isinstance(missing_indexes, list), "'missing_indexes' should be a list"
    assert len(missing_indexes) == 1, f"Expected exactly 1 missing index, got {len(missing_indexes)}"
    assert missing_indexes[0] == expected_index, f"Expected missing index statement '{expected_index}', got '{missing_indexes[0]}'"