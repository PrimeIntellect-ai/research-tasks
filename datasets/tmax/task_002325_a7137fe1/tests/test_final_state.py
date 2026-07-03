# test_final_state.py
import os

def test_etl_script_exists():
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"The ETL script is missing: {script_path}"

def test_clean_temperature_csv_content():
    csv_path = "/home/user/clean_temperature.csv"
    assert os.path.isfile(csv_path), f"The output CSV file is missing: {csv_path}"

    expected_lines = [
        "2023-10-01 10:00,22.5",
        "2023-10-01 10:01,22.8",
        "2023-10-01 10:02,23.0",
        "2023-10-01 10:03,23.0",
        "2023-10-01 10:04,23.0",
        "2023-10-01 10:05,23.5",
        "2023-10-01 10:06,23.6",
        "2023-10-01 10:07,23.6",
        "2023-10-01 10:08,23.6",
        "2023-10-01 10:09,24.0",
        "2023-10-01 10:10,24.1"
    ]

    with open(csv_path, "r") as f:
        actual_content = f.read().strip().splitlines()

    assert len(actual_content) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(actual_content)} in {csv_path}"

    for i, (actual, expected) in enumerate(zip(actual_content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"