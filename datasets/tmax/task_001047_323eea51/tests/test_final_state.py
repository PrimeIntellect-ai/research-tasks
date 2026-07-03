# test_final_state.py
import os
import pytest

def test_hourly_averages_file_exists():
    path = "/home/user/hourly_averages.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Ensure the script was run and generated the output file."

def test_hourly_averages_content():
    path = "/home/user/hourly_averages.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected_lines = [
        "Hour: 00, Avg: 100",
        "Hour: 01, Avg: 250",
        "Hour: 02, Avg: 150",
        "Hour: 11, Avg: 120",
        "Hour: 12, Avg: 140",
        "Hour: 17, Avg: 50"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {path} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )