# test_final_state.py
import os
import json
import pytest

def test_uptime_report_exists_and_correct():
    report_path = "/home/user/app/uptime_report.json"
    wal_path = "/home/user/data/tracker.wal"

    assert os.path.isfile(wal_path), f"WAL file {wal_path} is missing."
    assert os.path.isfile(report_path), f"Report file {report_path} was not generated."

    # Derive expected values from the WAL file
    expected_total = 0
    expected_up = 0

    with open(wal_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                expected_total += 1
                if entry.get("status") == "up":
                    expected_up += 1
            except json.JSONDecodeError:
                # Skip corrupted lines as expected by the application logic
                pass

    # Read the generated report
    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} does not contain valid JSON.")

    # Assert the structure and values
    assert "total_processed" in report_data, "Report is missing 'total_processed' key."
    assert "up_count" in report_data, "Report is missing 'up_count' key."

    actual_total = report_data["total_processed"]
    actual_up = report_data["up_count"]

    assert actual_total == expected_total, f"Expected total_processed to be {expected_total}, but got {actual_total}."
    assert actual_up == expected_up, f"Expected up_count to be {expected_up}, but got {actual_up}."