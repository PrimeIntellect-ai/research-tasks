# test_final_state.py

import os
import pytest

def test_report_exists():
    assert os.path.isfile("/home/user/report.txt"), "The report file /home/user/report.txt does not exist."

def test_report_content():
    with open("/home/user/report.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(lines) >= 2, "The report file does not contain enough lines. Expected exactly 2 lines."

    log_id = lines[0]
    func_name = lines[1]

    assert log_id == "B2", f"Line 1 of the report is incorrect. Expected 'B2', got '{log_id}'."
    assert func_name == "calculate_msg_len", f"Line 2 of the report is incorrect. Expected 'calculate_msg_len', got '{func_name}'."