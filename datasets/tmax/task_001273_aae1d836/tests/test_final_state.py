# test_final_state.py

import os
import re
import math
import pytest

def test_rejected_log_exists_and_correct():
    """Test that rejected.log exists and contains the exact expected malformed lines."""
    rejected_path = '/home/user/output/rejected.log'
    assert os.path.isfile(rejected_path), f"File {rejected_path} does not exist. Did the program run and create it?"

    expected_lines = [
        "A,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\n",
        "9,1.0,2.0,3.0\n"
    ]

    with open(rejected_path, 'r') as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"Contents of {rejected_path} do not match the expected rejected lines.\n"
        f"Expected: {expected_lines}\nActual: {actual_lines}"
    )

def test_duplicates_csv_exists_and_correct():
    """Test that duplicates.csv exists and contains the expected duplicate pairs."""
    duplicates_path = '/home/user/output/duplicates.csv'
    assert os.path.isfile(duplicates_path), f"File {duplicates_path} does not exist."

    # We expect 3 pairs based on the data:
    # 1 and 3: cos_sim = (1.0*0.99) / (1.0 * sqrt(0.99^2 + 0.141^2)) = 0.99 / 1.00004 = 0.98996 -> rounds to 0.9900
    # 2 and 7: cos_sim = 0.99 / 1.00004 = 0.98996 -> 0.9900
    # 5 and 8: cos_sim = 0.98 / sqrt(0.98^2 + 0.199^2) = 0.98 / 1.000005 = 0.97999 -> 0.9800

    expected_pairs = [
        "1,3,0.9900",
        "2,7,0.9900",
        "5,8,0.9800"
    ]

    with open(duplicates_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_pairs), (
        f"Expected {len(expected_pairs)} duplicate pairs, but found {len(actual_lines)}."
    )

    for expected, actual in zip(expected_pairs, actual_lines):
        assert actual == expected, (
            f"Mismatch in duplicate pair.\nExpected: {expected}\nActual: {actual}"
        )

def test_benchmark_txt_exists_and_format():
    """Test that benchmark.txt exists and matches the expected format."""
    benchmark_path = '/home/user/output/benchmark.txt'
    assert os.path.isfile(benchmark_path), f"File {benchmark_path} does not exist."

    with open(benchmark_path, 'r') as f:
        content = f.read().strip()

    pattern = r"^Search took [0-9]+\.[0-9]{6} seconds\.$"
    assert re.match(pattern, content), (
        f"Contents of {benchmark_path} do not match the expected format.\n"
        f"Expected pattern: {pattern}\nActual: '{content}'"
    )