# test_final_state.py

import os
import pytest

def test_clean_logs_csv_content():
    file_path = "/home/user/clean_logs.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "timestamp,service_name,user_email,changes_count",
        "1700000000,nginx,***@acme.corp,5",
        "1700000060,sshd,***@acme.corp,5",
        "1700000120,nginx,***@acme.corp,10",
        "1700000180,postgres,***@acme.corp,10",
        "1700000240,redis,***@acme.corp,3"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} is incorrect.\nExpected: {expected}\nGot: {actual}"

def test_summary_log_content():
    file_path = "/home/user/summary.log"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Total Changes: 33"
    assert content == expected_content, f"Content of {file_path} is incorrect.\nExpected: '{expected_content}'\nGot: '{content}'"