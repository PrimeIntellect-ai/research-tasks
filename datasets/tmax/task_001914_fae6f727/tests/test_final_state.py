# test_final_state.py
import os
import pytest

def test_cleaned_data_csv():
    file_path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. Did the Rust program run and produce the output?"

    expected_lines = [
        "sensor_id,successes,trials",
        "1,10,20",
        "2,15,30",
        "3,12,25",
        "4,5,10",
        "5,19,40"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    # Normalize carriage returns if any
    content = [line.strip() for line in content if line.strip()]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} is incorrect. Expected '{expected}', got '{actual}'."

def test_metrics_txt():
    file_path = "/home/user/metrics.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. Did the Rust program generate the metrics log?"

    expected_lines = [
        "Posterior Alpha: 32.0000",
        "Posterior Beta: 35.0000",
        "Posterior Mean: 0.4776"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    content = [line.strip() for line in content if line.strip()]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} is incorrect. Expected '{expected}', got '{actual}'."