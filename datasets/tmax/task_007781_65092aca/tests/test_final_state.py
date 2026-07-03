# test_final_state.py

import os
import csv
import pytest

def test_pipeline_files_exist():
    """Ensure the pipeline script and C program exist."""
    assert os.path.isfile("/home/user/pipeline.sh"), "Missing /home/user/pipeline.sh"
    assert os.path.isfile("/home/user/interpolate.c"), "Missing /home/user/interpolate.c"

def test_csv_output_exists():
    """Ensure the output CSV file is created."""
    csv_path = "/home/user/clean_resampled.csv"
    assert os.path.isfile(csv_path), f"Missing output file: {csv_path}"

def test_csv_output_content():
    """Ensure the output CSV contains the correct interpolated values."""
    csv_path = "/home/user/clean_resampled.csv"
    if not os.path.isfile(csv_path):
        pytest.fail(f"File {csv_path} does not exist.")

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 5, f"Expected at least a header and 4 rows, found {len(rows)} rows."

    # Check header
    assert rows[0] == ["timestamp", "temperature"], f"Incorrect CSV header: {rows[0]}"

    # Expected values
    expected = {
        "1696161610": 18.00,
        "1696161620": 20.33,
        "1696161630": 15.00,
        "1696161640": 25.00
    }

    parsed_data = {}
    for row in rows[1:]:
        if not row:
            continue
        assert len(row) == 2, f"Invalid row format: {row}"
        ts, temp_str = row
        try:
            parsed_data[ts] = float(temp_str)
        except ValueError:
            pytest.fail(f"Invalid temperature value: {temp_str}")

    for ts, expected_temp in expected.items():
        assert ts in parsed_data, f"Missing timestamp {ts} in output CSV."
        actual_temp = parsed_data[ts]
        assert abs(actual_temp - expected_temp) < 0.05, f"For timestamp {ts}, expected temp ~{expected_temp:.2f}, got {actual_temp}"