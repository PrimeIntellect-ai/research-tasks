# test_final_state.py

import os
import csv
import pytest

def test_metrics_csv_exists_and_content():
    file_path = "/home/user/metrics.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{file_path} is empty."

    headers = rows[0]
    expected_headers = ["DeviceID", "Architecture", "MatrixSize", "InferenceTimeMS", "GigaFLOPS"]
    assert headers == expected_headers, f"Headers in {file_path} do not match expected. Got: {headers}"

    data_rows = rows[1:]
    assert len(data_rows) == 7, f"Expected 7 valid data rows in {file_path}, but got {len(data_rows)}."

    # Create a set of tuples for expected rows to ignore order
    expected_data = {
        ("DEV1", "ARM64", "1024", "15.5", "138.547"),
        ("DEV2", "x86", "2048", "120.0", "143.166"),
        ("DEV3", "ARM64", "512", "2.1", "127.826"),
        ("DEV1", "ARM64", "1024", "16.2", "132.561"),
        ("DEV4", "RISCV", "256", "0.8", "41.943"),
        ("DEV5", "ARM64", "1024", "14.9", "144.126"),
        ("DEV5", "ARM64", "2048", "125.4", "137.001")
    }

    actual_data = set(tuple(row) for row in data_rows)

    missing = expected_data - actual_data
    extra = actual_data - expected_data

    assert not missing, f"Missing expected rows in {file_path}: {missing}"
    assert not extra, f"Unexpected extra rows in {file_path}: {extra}"

def test_bootstrap_arm64_exists_and_content():
    file_path = "/home/user/bootstrap_arm64.txt"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"{file_path} is empty."

    try:
        bootstrap_mean = float(content)
    except ValueError:
        pytest.fail(f"Content of {file_path} is not a valid float: '{content}'")

    # True Mean: (138.547 + 127.826 + 132.561 + 144.126 + 137.001) / 5 = 136.012
    # Allowance: +/- 1.5
    lower_bound = 136.012 - 1.5
    upper_bound = 136.012 + 1.5

    assert lower_bound <= bootstrap_mean <= upper_bound, \
        f"Bootstrap mean {bootstrap_mean} is outside the acceptable range [{lower_bound}, {upper_bound}]."