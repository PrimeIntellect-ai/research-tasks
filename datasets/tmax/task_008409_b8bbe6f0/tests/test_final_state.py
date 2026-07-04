# test_final_state.py
import os
import csv
import subprocess
import pytest

def test_makefile_and_etl_script_exist():
    assert os.path.isfile("/home/user/Makefile"), "Makefile is missing in /home/user/"
    assert os.path.isfile("/home/user/etl.py"), "etl.py is missing in /home/user/"

def test_make_run_and_output():
    output_file = "/home/user/output/final_metrics.csv"

    # Ensure starting clean if the test is run multiple times
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run make run
    result = subprocess.run(["make", "run"], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"'make run' failed with error:\n{result.stderr}"

    assert os.path.isfile(output_file), f"Output file {output_file} was not created."

    # Read the CSV
    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."

    # Strip whitespace from headers
    headers = [h.strip() for h in rows[0]]
    expected_headers = ["timestamp", "ip_address", "datacenter", "cpu_percent", "mem_percent"]
    assert headers == expected_headers, f"Headers are incorrect. Expected {expected_headers}, got {headers}"

    data_rows = [[c.strip() for c in row] for row in rows[1:]]

    expected_data = [
        ["2023-10-01T10:00:00Z", "10.0.0.1", "us-east-1", "50.0", "50.0"],
        ["2023-10-01T10:00:00Z", "10.0.0.2", "eu-west-1", "10.0", "12.5"],
        ["2023-10-01T10:05:00Z", "10.0.0.1", "us-east-1", "60.0", "53.1"],
        ["2023-10-01T10:05:00Z", "10.0.0.3", "ap-south-1", "90.0", "100.0"]
    ]

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, but got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"

    # Test idempotency
    with open(output_file, 'r') as f:
        content_before = f.read()

    result_again = subprocess.run(["make", "run"], cwd="/home/user", capture_output=True, text=True)
    assert result_again.returncode == 0, f"Second 'make run' failed with error:\n{result_again.stderr}"

    with open(output_file, 'r') as f:
        content_after = f.read()

    assert content_before == content_after, "Pipeline is not idempotent. Output changed or duplicated after second run."