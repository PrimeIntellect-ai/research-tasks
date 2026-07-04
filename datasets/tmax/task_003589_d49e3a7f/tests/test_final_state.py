# test_final_state.py

import os
import pytest

def test_files_exist():
    """Verify that the required script and C program files exist."""
    assert os.path.exists("/home/user/resample.c"), "/home/user/resample.c is missing."
    assert os.path.exists("/home/user/run_pipeline.sh"), "/home/user/run_pipeline.sh is missing."
    assert os.path.exists("/home/user/processed_sensors.tsv"), "/home/user/processed_sensors.tsv is missing."

def test_processed_sensors_content():
    """Verify that the processed_sensors.tsv file has the exact expected content."""
    expected_lines = [
        "NewYork/NYC\t1672531200\t-2.00",
        "Paris/Île-de-France\t1672531200\t5.00",
        "Paris/Île-de-France\t1672534800\t6.00",
        "Paris/Île-de-France\t1672538400\t7.50",
        "Tokyo/東京\t1672531200\t11.00",
        "Tokyo/東京\t1672534800\t11.00",
        "Tokyo/東京\t1672538400\t11.00",
        "Tokyo/東京\t1672542000\t9.00"
    ]

    file_path = "/home/user/processed_sensors.tsv"
    with open(file_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )