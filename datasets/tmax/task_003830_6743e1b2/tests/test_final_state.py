# test_final_state.py

import os
import pytest

def test_crash_report_content():
    report_path = "/home/user/crash_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Crashed at: TX-999"
    assert content == expected_content, f"Expected '{expected_content}' in {report_path}, but got '{content}'."

def test_reconstructed_timeline_content():
    log_path = "/home/user/reconstructed_timeline.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run the log_parser.py script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "TX-001",
        "TX-002",
        "TX-003",
        "TX-997",
        "TX-998",
        "TX-999",
        "[CORRUPTED]"
    ]

    assert lines == expected_lines, (
        f"Contents of {log_path} do not match the expected timeline.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )

def test_log_parser_modified():
    parser_path = "/home/user/log_parser.py"
    assert os.path.isfile(parser_path), f"File {parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    assert "[CORRUPTED]" in content, f"The string '[CORRUPTED]' was not found in {parser_path}. Ensure you updated the script to handle circular references."