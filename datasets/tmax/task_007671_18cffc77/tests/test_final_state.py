# test_final_state.py

import os
import json
import pytest

def test_debug_report_exists_and_valid():
    report_path = "/home/user/debug_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    assert "recovered_secret" in report, "Missing 'recovered_secret' in report"
    assert report["recovered_secret"] == "xtk_99281_devops_secret", "Incorrect 'recovered_secret'"

    assert "blocking_file" in report, "Missing 'blocking_file' in report"
    assert report["blocking_file"] == "/tmp/config_pipe", "Incorrect 'blocking_file'"

    assert "critical_auth_count" in report, "Missing 'critical_auth_count' in report"
    assert report["critical_auth_count"] == 2, "Incorrect 'critical_auth_count'"

def test_processed_logs_csv():
    csv_path = "/home/user/processed_logs.csv"
    assert os.path.isfile(csv_path), f"Processed logs file {csv_path} does not exist"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines (1 header + 2 rows) in {csv_path}, but got {len(lines)}"

    expected_header = "timestamp,level,service,message"
    assert lines[0] == expected_header, f"Expected header '{expected_header}', got '{lines[0]}'"

    expected_rows = [
        "2023-10-01T10:01:00,CRITICAL,auth,Authentication bypassed",
        "2023-10-01T10:03:00,CRITICAL,auth,Multiple failed logins"
    ]

    for row in expected_rows:
        assert row in lines, f"Expected row '{row}' not found in {csv_path}"