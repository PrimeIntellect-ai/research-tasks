# test_final_state.py

import os
import csv

def test_similarity_report_exists_and_correct():
    report_path = "/home/user/similarity_report.csv"
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."

    expected_rows = [
        ["timestamp1", "timestamp2", "jaccard_similarity"],
        ["2023-10-01T00", "2023-10-01T01", "1.0000"],
        ["2023-10-01T01", "2023-10-01T02", "0.2000"],
        ["2023-10-01T02", "2023-10-01T03", "1.0000"],
        ["2023-10-01T03", "2023-10-01T04", "1.0000"],
        ["2023-10-01T04", "2023-10-01T05", "0.5000"],
    ]

    with open(report_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), (
        f"Expected {len(expected_rows)} rows in the CSV, but found {len(actual_rows)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, (
            f"Row {i + 1} does not match. Expected: {expected}, Got: {actual}"
        )

def test_script_exists():
    script_path = "/home/user/analyze_configs.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."