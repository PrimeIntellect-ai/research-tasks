# test_final_state.py

import os
import json
import pytest

def test_report_json_exists():
    """Test that the /home/user/report.json file exists."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

def test_report_json_content():
    """Test that the report.json contains the correct active_wal and purge_candidates."""
    report_path = "/home/user/report.json"

    try:
        with open(report_path, "r") as f:
            report_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "active_wal" in report_data, "The JSON report is missing the 'active_wal' key."
    assert "purge_candidates" in report_data, "The JSON report is missing the 'purge_candidates' key."

    assert report_data["active_wal"] == "db_7.wal", f"Expected active_wal to be 'db_7.wal', but got '{report_data['active_wal']}'."

    expected_candidates = ["db_2.wal", "db_6.wal"]
    actual_candidates = report_data["purge_candidates"]

    assert isinstance(actual_candidates, list), "'purge_candidates' must be a JSON array (list)."
    assert sorted(actual_candidates) == expected_candidates, f"Expected purge_candidates to be {expected_candidates}, but got {actual_candidates}."