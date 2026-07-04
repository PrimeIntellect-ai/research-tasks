# test_final_state.py

import os
import struct
import pytest

def to_float32(val):
    """Simulate IEEE 754 32-bit float casting."""
    return struct.unpack('f', struct.pack('f', float(val)))[0]

def compute_expected_failing_row():
    """Derive the exact failing row using float32 simulation."""
    count = to_float32(0.0)
    sum_val = to_float32(0.0)
    sum_sq = to_float32(0.0)

    for i in range(1, 10001):
        val = to_float32(10000.0 if i % 2 != 0 else 10000.1)
        count = to_float32(count + to_float32(1.0))
        sum_val = to_float32(sum_val + val)
        sum_sq = to_float32(sum_sq + to_float32(val * val))

        mean = to_float32(sum_val / count)
        variance = to_float32(to_float32(sum_sq / count) - to_float32(mean * mean))

        if variance < 0:
            return i
    return -1

def test_failing_row():
    """Verify that failing_row.txt contains the correct 1-indexed row count."""
    file_path = "/home/user/data_processor/failing_row.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_row = compute_expected_failing_row()
    assert expected_row > 0, "Failed to compute expected failing row in test."

    assert content == str(expected_row), f"Expected failing row {expected_row}, but got '{content}'."

def test_final_result():
    """Verify that final_result.txt contains the correct standard deviation."""
    file_path = "/home/user/data_processor/final_result.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "0.050000"
    assert content == expected, f"Expected final result '{expected}', but got '{content}'."

def test_processor_executable():
    """Verify that the processor executable exists and is executable."""
    file_path = "/home/user/data_processor/processor"
    assert os.path.isfile(file_path), f"Executable {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."