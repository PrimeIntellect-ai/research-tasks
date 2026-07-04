# test_final_state.py

import os
import pytest

def test_workspace_exists():
    assert os.path.exists("/home/user/workspace"), "/home/user/workspace directory does not exist."
    assert os.path.isdir("/home/user/workspace"), "/home/user/workspace is not a directory."

def test_c_program_exists():
    c_file = "/home/user/workspace/config_analyzer.c"
    assert os.path.exists(c_file), f"{c_file} does not exist."
    assert os.path.isfile(c_file), f"{c_file} is not a file."

def test_report_csv_exists_and_content():
    report_file = "/home/user/workspace/report.csv"
    assert os.path.exists(report_file), f"{report_file} does not exist."
    assert os.path.isfile(report_file), f"{report_file} is not a file."

    expected_content = """Date,FilePath,TotalChanges,NetSizeDiff
2023-10-14,/etc/hosts,1,20
2023-10-14,/etc/nginx/nginx.conf,2,60
2023-10-14,/etc/ssh/sshd_config,1,-1200
2023-10-15,/etc/hosts,1,-5
2023-10-15,/etc/nginx/nginx.conf,1,-20
2023-10-15,/etc/sudoers,1,10
2023-10-16,/etc/passwd,1,80
"""

    with open(report_file, 'r') as f:
        actual_content = f.read()

    # Strip trailing whitespace and normalize line endings for comparison
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]

    assert actual_lines == expected_lines, "The content of report.csv does not match the expected output."