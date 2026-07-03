# test_final_state.py

import os
import pytest

def test_success_file_exists_and_contains_expected_text():
    success_file = "/home/user/success.txt"
    assert os.path.exists(success_file), f"The file {success_file} was not created. The exploit may have failed or written to the wrong location."
    assert os.path.isfile(success_file), f"{success_file} exists but is not a file."

    with open(success_file, 'r') as f:
        content = f.read().strip()

    assert content == "EXPLOITED", f"The content of {success_file} is incorrect. Expected 'EXPLOITED', got '{content}'."

def test_report_file_exists_and_contains_correct_info():
    report_file = "/home/user/report.txt"
    assert os.path.exists(report_file), f"The report file {report_file} was not created."
    assert os.path.isfile(report_file), f"{report_file} exists but is not a file."

    with open(report_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"The report file should contain exactly 3 non-empty lines, but found {len(lines)}."

    assert lines[0] == "CWE-22", f"Line 1 of report.txt is incorrect. Expected 'CWE-22' (Path Traversal), got '{lines[0]}'."
    assert lines[1] == "Sup3rS3cr3tK3y!!", f"Line 2 of report.txt (AES Key) is incorrect. Got '{lines[1]}'."
    assert lines[2] == "1n1t1alV3ct0r123", f"Line 3 of report.txt (AES IV) is incorrect. Got '{lines[2]}'."

def test_exploit_file_exists():
    exploit_file = "/home/user/exploit.cpp"
    assert os.path.exists(exploit_file), f"The exploit source file {exploit_file} does not exist."
    assert os.path.isfile(exploit_file), f"{exploit_file} exists but is not a file."