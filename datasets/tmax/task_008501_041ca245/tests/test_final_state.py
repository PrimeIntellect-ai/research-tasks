# test_final_state.py
import os
import pytest

def test_data_out_exists():
    path = "/home/user/data.out"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. The program may not have run successfully or still writes to the wrong path."

def test_data_out_contents():
    path = "/home/user/data.out"
    expected_lines = [
        "Sensor 101: 12345.678901",
        "Sensor 102: 98765.432109",
        "Sensor 103: 0.000001"
    ]

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'. Precision loss may still be present."

def test_telemetry_ingest_cpp_fixes():
    path = "/home/user/telemetry_ingest.cpp"
    assert os.path.isfile(path), f"Source file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/data.out" in content, "The source code does not contain the correct output path '/home/user/data.out'."
    assert "/root/telemetry.out" not in content, "The source code still contains the buggy output path '/root/telemetry.out'."
    assert "double" in content, "The source code does not seem to use 'double' to fix the precision loss."