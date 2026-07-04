# test_final_state.py
import os
import csv

def test_conflict_report_exists_and_correct():
    """Test that the conflict_report.csv file exists and contains the correct data."""
    report_path = "/home/user/conflict_report.csv"
    assert os.path.isfile(report_path), f"Expected output file is missing: {report_path}"

    expected_data = [
        ["http://example.org/audit#emp3", "http://example.org/audit#vendor3", "http://example.org/audit#sysC"],
        ["http://example.org/audit#emp1", "http://example.org/audit#vendor1", "http://example.org/audit#sysA"]
    ]

    actual_data = []
    with open(report_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # skip empty lines if any
                actual_data.append(row)

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows, but got {len(actual_data)}."

    for i, (actual_row, expected_row) in enumerate(zip(actual_data, expected_data)):
        assert actual_row == expected_row, f"Row {i+1} mismatch. Expected {expected_row}, got {actual_row}."

def test_find_conflicts_script_exists():
    """Test that the student's script was created."""
    script_path = "/home/user/find_conflicts.py"
    assert os.path.isfile(script_path), f"Expected script file is missing: {script_path}"