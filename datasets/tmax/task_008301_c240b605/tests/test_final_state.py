# test_final_state.py

import os
import pytest

def test_process_logs_cpp_exists():
    """Test that the C++ source file was created."""
    cpp_file = "/home/user/process_logs.cpp"
    assert os.path.isfile(cpp_file), f"Missing C++ source file at {cpp_file}"

def test_hourly_stats_csv_exists():
    """Test that the hourly_stats.csv file was generated."""
    csv_file = "/home/user/hourly_stats.csv"
    assert os.path.isfile(csv_file), f"Missing generated CSV file at {csv_file}"

def test_hourly_stats_csv_content():
    """Test that the generated CSV file has the correct content."""
    csv_file = "/home/user/hourly_stats.csv"

    expected_lines = [
        "Hour,Avg_Latency",
        "08,125.00",
        "09,205.00",
        "10,55.00",
        "23,999.00"
    ]

    with open(csv_file, "r") as f:
        # Read lines and strip trailing newlines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {csv_file} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )