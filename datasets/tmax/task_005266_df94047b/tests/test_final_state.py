# test_final_state.py

import os
import pytest

def test_output_file_exists():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file is missing: {path}"

def test_output_file_contents():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file is missing: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Timestamp: 100, Lat: 37.7749, Lon: -122.4194",
        "Timestamp: 101, Lat: 34.0522, Lon: -118.2437",
        "Timestamp: 103, Lat: 40.7128, Lon: -74.0060",
        "Timestamp: 104, Lat: 51.5074, Lon: -0.1278",
        "Timestamp: 106, Lat: 48.8566, Lon: 2.3522",
        "Timestamp: 107, Lat: 35.6895, Lon: 139.6917",
        "Timestamp: 108, Lat: -33.8688, Lon: 151.2093",
        "Timestamp: 109, Lat: 55.7558, Lon: 37.6173",
        "Timestamp: 110, Lat: -23.5505, Lon: -46.6333",
        "Timestamp: 111, Lat: -37.8136, Lon: 144.9631"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_process_script_fixes():
    path = "/home/user/process.py"
    assert os.path.isfile(path), f"Python script is missing: {path}"

    with open(path, 'r') as f:
        content = f.read()

    # Check that the old buggy unpack string is gone
    assert "<I I f f 8x" not in content, "The script still contains the incorrect struct unpacking format '<I I f f 8x'."