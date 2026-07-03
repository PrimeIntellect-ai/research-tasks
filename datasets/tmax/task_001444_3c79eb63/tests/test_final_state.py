# test_final_state.py

import os
import csv

def test_c_program_exists():
    c_source = "/home/user/log_processor.c"
    c_binary = "/home/user/log_processor"

    assert os.path.exists(c_source), f"The C source file {c_source} does not exist."
    assert os.path.exists(c_binary), f"The compiled binary {c_binary} does not exist."
    assert os.access(c_binary, os.X_OK), f"The file {c_binary} is not executable."

def test_hourly_stats_exists():
    stats_file = "/home/user/hourly_stats.csv"
    assert os.path.exists(stats_file), f"The output file {stats_file} does not exist."
    assert os.path.isfile(stats_file), f"The path {stats_file} is not a file."

def test_hourly_stats_content():
    stats_file = "/home/user/hourly_stats.csv"

    expected_content = [
        ["472222", "U1", "2", "175"],
        ["472222", "U2", "1", "50"],
        ["472223", "U1", "1", "300"],
        ["472223", "U4", "1", "0"],
        ["472224", "U4", "1", "10"]
    ]

    actual_content = []
    with open(stats_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_content.append(row)

    assert actual_content == expected_content, (
        f"The contents of {stats_file} do not match the expected output.\n"
        f"Expected: {expected_content}\n"
        f"Actual: {actual_content}"
    )