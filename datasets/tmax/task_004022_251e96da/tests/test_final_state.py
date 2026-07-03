# test_final_state.py

import os

def test_clean_metrics_csv_content():
    """Check if the clean_metrics.csv file exists and has the exact expected content."""
    csv_file_path = "/home/user/clean_metrics.csv"
    assert os.path.exists(csv_file_path), f"File {csv_file_path} is missing. The Go program likely did not run or output to the correct path."
    assert os.path.isfile(csv_file_path), f"{csv_file_path} is not a file."

    expected_content = (
        "Timestamp,Endpoint,ResponseTimeMs,ServerLoad\n"
        "2023-10-01T10:00:00Z,/api/v1/data,45,0.55\n"
        "2023-10-01T10:01:00Z,/api/v1/users,120,0.60\n"
        "2023-10-01T10:02:00Z,/api/v1/status,10,0.65\n"
        "2023-10-01T10:04:00Z,/api/v1/data,50,0.75\n"
        "2023-10-01T10:05:00Z,/api/v1/settings,30,0.80\n"
        "2023-10-01T10:06:00Z,/api/v1/profile,80,0.85"
    )

    with open(csv_file_path, "r") as f:
        content = f.read().strip()

    # Compare lines to give better error messages
    expected_lines = expected_content.split("\n")
    actual_lines = content.split("\n")

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in the CSV, but found {len(actual_lines)}."
    )

    for i, (expected_line, actual_line) in enumerate(zip(expected_lines, actual_lines)):
        assert actual_line.strip() == expected_line.strip(), (
            f"Mismatch at line {i+1}.\nExpected: {expected_line}\nFound:    {actual_line}"
        )