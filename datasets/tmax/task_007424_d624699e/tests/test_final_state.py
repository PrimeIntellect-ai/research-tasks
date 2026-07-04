# test_final_state.py
import os
import re
import pytest

def test_script_exists():
    script_path = '/home/user/profile_gc.py'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_report_exists():
    report_path = '/home/user/report.txt'
    assert os.path.exists(report_path), f"The report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_report_content():
    report_path = '/home/user/report.txt'
    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(lines)}."

    naive_match = re.match(r'^Naive:\s*([+-]?\d*\.\d+e[+-]\d+)$', lines[0], re.IGNORECASE)
    assert naive_match, f"Line 1 does not match the expected format 'Naive: <value>': {lines[0]}"

    stable_match = re.match(r'^Stable:\s*([+-]?\d*\.\d+e[+-]\d+)$', lines[1], re.IGNORECASE)
    assert stable_match, f"Line 2 does not match the expected format 'Stable: <value>': {lines[1]}"

    naive_val = float(naive_match.group(1))
    stable_val = float(stable_match.group(1))

    assert naive_val == 0.0, f"Expected Naive variance to be 0.0, got {naive_val}"
    assert abs(stable_val - 9.99e-08) < 1e-10, f"Expected Stable variance to be approx 9.99e-08, got {stable_val}"

    # Also check the exact formatting to 10 decimal places in scientific notation
    assert "0.0000000000e+00" in lines[0] or "0.0000000000e-00" in lines[0] or naive_match.group(1) == "0.0000000000e+00", f"Naive value not formatted to 10 decimal places in scientific notation: {lines[0]}"
    assert "9.9900000000e-08" in lines[1], f"Stable value not formatted to 10 decimal places in scientific notation: {lines[1]}"