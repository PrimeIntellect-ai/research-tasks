# test_final_state.py

import os
import pytest

def test_directories_exist():
    """Check if the organized directories exist."""
    assert os.path.isdir("/home/user/organized/low_error"), "Directory /home/user/organized/low_error is missing."
    assert os.path.isdir("/home/user/organized/high_error"), "Directory /home/user/organized/high_error is missing."

def test_files_moved_correctly():
    """Check if the CSV files were moved to the correct directories."""
    low_error_files = ["dataset_A.csv", "dataset_B.csv"]
    high_error_files = ["dataset_C.csv"]

    for filename in low_error_files:
        filepath = f"/home/user/organized/low_error/{filename}"
        assert os.path.isfile(filepath), f"File {filename} should be in /home/user/organized/low_error/."
        assert not os.path.exists(f"/home/user/datasets/{filename}"), f"File {filename} should have been moved from /home/user/datasets/."

    for filename in high_error_files:
        filepath = f"/home/user/organized/high_error/{filename}"
        assert os.path.isfile(filepath), f"File {filename} should be in /home/user/organized/high_error/."
        assert not os.path.exists(f"/home/user/datasets/{filename}"), f"File {filename} should have been moved from /home/user/datasets/."

def test_metrics_txt_content():
    """Check if metrics.txt contains the correct output formatted properly."""
    metrics_file = "/home/user/organized/metrics.txt"
    assert os.path.isfile(metrics_file), f"File {metrics_file} is missing."

    expected_lines = [
        "dataset_A.csv: m=2.0000, b=1.0000, MSE=0.0000",
        "dataset_B.csv: m=2.1000, b=0.6000, MSE=0.1750",
        "dataset_C.csv: m=-1.4000, b=5.1000, MSE=12.0500"
    ]

    with open(metrics_file, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), "metrics.txt does not have the correct number of lines."

    for expected, actual in zip(expected_lines, actual_lines):
        assert actual == expected, f"Expected line '{expected}', but got '{actual}' in metrics.txt."