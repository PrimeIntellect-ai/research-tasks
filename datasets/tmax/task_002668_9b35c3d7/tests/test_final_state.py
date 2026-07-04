# test_final_state.py

import os
import subprocess
import pytest
import math

SCRIPT_PATH = "/home/user/process_etl.sh"
INPUT_PATH = "/home/user/incoming_data.csv"
OUTPUT_PATH = "/home/user/processed_data.csv"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_header = "id,v1,v2,v3,v4,l2_norm,dot_product,is_outlier"
    assert lines[0] == expected_header, f"Header is incorrect. Expected {expected_header}, got {lines[0]}"

    # We will compute the expected values for the initial input data
    # The input data from truth:
    # 1,1.0,2.0,3.0,4.0
    # 2,0.0,,0.0,0.0
    # 3,10.0,10.0,10.0,10.0
    # 4,-1.0,,-3.0,
    # 5,,2.5,,1.1

    raw_data = [
        ("1", "1.0", "2.0", "3.0", "4.0"),
        ("2", "0.0", "", "0.0", "0.0"),
        ("3", "10.0", "10.0", "10.0", "10.0"),
        ("4", "-1.0", "", "-3.0", ""),
        ("5", "", "2.5", "", "1.1"),
    ]

    expected_lines = [expected_header]
    w = [0.5, -0.5, 1.0, 2.0]

    for row in raw_data:
        id_val = row[0]
        v_vals = [float(x) if x != "" else 0.0 for x in row[1:]]

        l2_norm = math.sqrt(sum(x**2 for x in v_vals))
        dot_product = sum(x * y for x, y in zip(v_vals, w))
        is_outlier = 1 if l2_norm > 10.0000 else 0

        expected_line = f"{id_val},{v_vals[0]:.4f},{v_vals[1]:.4f},{v_vals[2]:.4f},{v_vals[3]:.4f},{l2_norm:.4f},{dot_product:.4f},{is_outlier}"
        expected_lines.append(expected_line)

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"