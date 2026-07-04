# test_final_state.py

import os
import math

def test_pipeline_script_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script is not executable: {script_path}"

def test_cleaned_data_content():
    cleaned_data_path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(cleaned_data_path), f"Cleaned data file not found: {cleaned_data_path}"

    expected_rows = [
        (1, 10.0, 2.0, 5.0, 15.0),
        (3, 15.0, 3.0, 5.0, 20.0),
        (4, 20.0, 4.0, 5.0, 25.0),
        (5, -5.0, 1.0, -5.0, -10.0),
        (6, 12.0, 2.0, 6.0, 18.0),
        (7, 9.0, -3.0, -3.0, -8.0),
        (8, 0.0, 5.0, 0.0, 2.0),
        (10, -10.0, -2.0, 5.0, 12.0)
    ]

    with open(cleaned_data_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_rows), f"Expected {len(expected_rows)} rows in cleaned data, found {len(lines)}"

    for i, (line, expected) in enumerate(zip(lines, expected_rows)):
        parts = line.split(",")
        assert len(parts) == 5, f"Row {i+1} does not have exactly 5 columns: {line}"

        try:
            parsed_row = (
                int(parts[0]),
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
                float(parts[4])
            )
        except ValueError:
            assert False, f"Row {i+1} contains invalid numerical values: {line}"

        assert parsed_row[0] == expected[0], f"Row {i+1} ID mismatch: expected {expected[0]}, got {parsed_row[0]}"
        for j in range(1, 5):
            assert math.isclose(parsed_row[j], expected[j], rel_tol=1e-4, abs_tol=1e-4), \
                f"Row {i+1} column {j+1} mismatch: expected {expected[j]}, got {parsed_row[j]}"

def test_correlation_output():
    correlation_path = "/home/user/correlation.txt"
    assert os.path.isfile(correlation_path), f"Correlation file not found: {correlation_path}"

    with open(correlation_path, "r") as f:
        content = f.read().strip()

    assert content == "0.9404", f"Correlation value incorrect: expected '0.9404', got '{content}'"