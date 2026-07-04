# test_final_state.py

import os
import pytest

def test_sensor_utf8_log():
    """Check that sensor_utf8.log exists and is UTF-8 encoded."""
    file_path = '/home/user/sensor_utf8.log'
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    try:
        with open(file_path, 'rb') as f:
            raw_bytes = f.read()
        # Decode as utf-8 should succeed
        content = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        pytest.fail(f"The file {file_path} is not properly encoded in UTF-8.")

    assert '[BEGIN]' in content, "The UTF-8 file does not contain expected content."

def test_sensor_clean_log():
    """Check that sensor_clean.log exists, has no \\r, and no leading/trailing spaces."""
    file_path = '/home/user/sensor_clean.log'
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        assert '\r' not in line, f"Line {i+1} in {file_path} contains a carriage return (\\r)."
        # Strip newline for leading/trailing check
        line_no_newline = line.strip('\n')
        if line_no_newline:
            assert line_no_newline == line_no_newline.strip(), f"Line {i+1} in {file_path} has leading or trailing spaces."

def test_cpp_file_exists():
    """Check that the C++ source file exists."""
    file_path = '/home/user/parse_logs.cpp'
    assert os.path.exists(file_path), f"The C++ program {file_path} is missing."

def test_clean_data_csv():
    """Check that clean_data.csv exists and contains the correct filtered data."""
    file_path = '/home/user/clean_data.csv'
    assert os.path.exists(file_path), f"The CSV file {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')

    expected = [
        "Timestamp,Station,Temp",
        "2023-05-12 08:00:00,Alpha,22.5",
        "2023-05-12 08:30:00,Alpha,23.1"
    ]

    assert len(content) == len(expected), f"Expected {len(expected)} lines in {file_path}, found {len(content)}."

    for i, (actual_line, expected_line) in enumerate(zip(content, expected)):
        assert actual_line.strip() == expected_line, f"Line {i+1} in {file_path} is incorrect. Expected '{expected_line}', got '{actual_line.strip()}'."