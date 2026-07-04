# test_final_state.py
import os
import struct
import pytest

def test_crash_time_extracted():
    crash_time_file = '/home/user/crash_time.txt'
    assert os.path.exists(crash_time_file), f"File {crash_time_file} does not exist."

    with open(crash_time_file, 'r') as f:
        content = f.read().strip()

    assert content == "1698394514", f"Expected crash time '1698394514', but got '{content}'."

def test_recovered_data_csv():
    csv_file = '/home/user/recovered_data.csv'
    assert os.path.exists(csv_file), f"File {csv_file} does not exist."

    with open(csv_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 5, "Recovered CSV file does not contain enough lines."
    assert lines[0] == "timestamp,sensor_id,temp_f", "CSV header is incorrect."

    expected_data = [
        "1698394400,1,68.00",
        "1698394410,2,77.00",
        "1698394420,1,72.50",
        "1698394430,3,86.00"
    ]

    for i, expected in enumerate(expected_data):
        assert lines[i+1] == expected, f"Line {i+2} in CSV is incorrect. Expected '{expected}', got '{lines[i+1]}'."

def test_utils_c_fixed():
    utils_c = '/home/user/src/utils.c'
    assert os.path.exists(utils_c), f"File {utils_c} does not exist."

    with open(utils_c, 'r') as f:
        content = f.read()

    # Check that the incorrect formula is gone and the correct one is present
    assert "(c * 5.0f / 9.0f)" not in content and "(c * 5 / 9)" not in content, "The bug in celsius_to_fahrenheit is still present."
    assert "9.0f / 5.0f" in content or "9 / 5.0" in content or "9.0 / 5" in content or "1.8" in content, "The corrected formula for celsius_to_fahrenheit was not found."

def test_makefile_fixed():
    makefile = '/home/user/src/Makefile'
    assert os.path.exists(makefile), f"File {makefile} does not exist."

    with open(makefile, 'r') as f:
        content = f.read()

    assert "-lm" in content, "The Makefile does not link the math library (-lm)."