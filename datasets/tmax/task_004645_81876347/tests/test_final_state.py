# test_final_state.py

import os
import re
import pytest

def test_source_code_exists():
    """Test that the C program source code exists."""
    assert os.path.exists("/home/user/extract_ts.c"), "The C source code file /home/user/extract_ts.c is missing."
    assert os.path.isfile("/home/user/extract_ts.c"), "/home/user/extract_ts.c is not a file."

def test_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.exists("/home/user/extract_ts"), "The compiled executable /home/user/extract_ts is missing."
    assert os.path.isfile("/home/user/extract_ts"), "/home/user/extract_ts is not a file."
    assert os.access("/home/user/extract_ts", os.X_OK), "/home/user/extract_ts is not executable."

def test_output_file_exists():
    """Test that the output CSV file exists."""
    assert os.path.exists("/home/user/fr_menu_ts.csv"), "The output file /home/user/fr_menu_ts.csv is missing."
    assert os.path.isfile("/home/user/fr_menu_ts.csv"), "/home/user/fr_menu_ts.csv is not a file."

def test_output_contents():
    """Test that the output file contains the correctly processed data."""
    input_file = "/home/user/loc_logs.csv"
    output_file = "/home/user/fr_menu_ts.csv"

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    expected_rows = []
    pattern = re.compile(r"^menu_[a-z]+_[0-9]+$")

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            ts_str, loc, key, rt_str = parts
            try:
                ts = int(ts_str)
                rt = int(rt_str)
            except ValueError:
                continue

            if loc != "fr_FR":
                continue

            if not pattern.match(key):
                continue

            ts_hour = (ts // 3600) * 3600
            cat = "FAST" if rt < 100 else "SLOW"
            expected_rows.append(f"{ts_hour},{key},{cat}")

    with open(output_file, "r") as f:
        actual_rows = [line.strip() for line in f if line.strip()]

    assert len(actual_rows) == len(expected_rows), f"Row count mismatch. Expected {len(expected_rows)}, got {len(actual_rows)}."

    for i, (exp, act) in enumerate(zip(expected_rows, actual_rows)):
        assert exp == act, f"Mismatch at line {i+1}: expected '{exp}', got '{act}'."