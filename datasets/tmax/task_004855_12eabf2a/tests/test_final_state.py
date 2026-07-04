# test_final_state.py

import os
import pytest

def test_config_file_exists():
    config_path = '/home/user/.local/share/sensor/default.conf'
    assert os.path.isfile(config_path), f"Expected configuration file {config_path} to be created."

def test_final_report_exists():
    report_path = '/home/user/final_report.txt'
    assert os.path.isfile(report_path), f"Expected final report {report_path} to be created."

def test_final_report_no_warnings():
    report_path = '/home/user/final_report.txt'
    with open(report_path, 'r') as f:
        content = f.read()
    assert "Warning" not in content, "The final report contains 'Warning', which means the configuration file wasn't properly detected or placed."

def test_final_report_no_negative_varsum():
    report_path = '/home/user/final_report.txt'
    with open(report_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "VarSum:-" in line:
            pytest.fail(f"Found a negative VarSum in the final report, which indicates the integer overflow was not fixed. Line: {line.strip()}")

def test_final_report_correct_varsum_for_extreme_file():
    report_path = '/home/user/final_report.txt'
    expected_substring = "file_00.dat Mean:0 VarSum:5400000000"

    with open(report_path, 'r') as f:
        content = f.read()

    assert expected_substring in content, f"Expected to find '{expected_substring}' in {report_path}. The overflow fix might be incorrect or the script was not run properly."