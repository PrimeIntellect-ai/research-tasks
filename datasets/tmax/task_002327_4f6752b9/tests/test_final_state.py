# test_final_state.py

import os
import pytest

def test_final_report_exists():
    assert os.path.isfile("/home/user/final_report.txt"), "The file /home/user/final_report.txt does not exist."

def test_final_report_contents():
    with open("/home/user/final_report.txt", "r") as f:
        content = f.read()

    expected_lines = [
        "Processed 2 records from /home/user/uploads/valid1.log",
        "Processed 3 records from /home/user/uploads/file with spaces.log",
        "Corrupted input: /home/user/uploads/corrupt.log",
        "Corrupted input: /home/user/uploads/massive.log"
    ]

    for line in expected_lines:
        assert line in content, f"Expected output not found in /home/user/final_report.txt: '{line}'"

def test_no_segfaults_in_error_log():
    error_log_path = "/home/user/pipeline/error.log"
    if os.path.isfile(error_log_path):
        with open(error_log_path, "r") as f:
            content = f.read().lower()
            assert "segmentation fault" not in content, "A Segmentation Fault was recorded in error.log."
            assert "segfault" not in content, "A Segfault was recorded in error.log."

def test_parser_c_fixed():
    parser_src = "/home/user/pipeline/parser.c"
    assert os.path.isfile(parser_src), f"Source file {parser_src} is missing."
    with open(parser_src, "r") as f:
        content = f.read()

    assert "Corrupted input:" in content, "The C code does not seem to print 'Corrupted input:' as requested."
    assert "10000" in content, "The C code does not seem to check the upper bound of 10000 for N."

def test_shell_script_fixed():
    script_src = "/home/user/pipeline/process_logs.sh"
    assert os.path.isfile(script_src), f"Script file {script_src} is missing."
    with open(script_src, "r") as f:
        content = f.read()

    assert "$(ls" not in content, "The shell script still uses the buggy `$(ls ...)` construct which breaks on spaces."