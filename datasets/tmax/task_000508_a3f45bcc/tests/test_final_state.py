# test_final_state.py
import os
import pytest

REPORT_PATH = '/home/user/deadlock_report.txt'

def test_deadlock_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

def test_deadlock_report_content():
    with open(REPORT_PATH, 'r') as f:
        content = f.read().strip()

    assert content == "101,102,103", f"Expected '101,102,103', but got '{content}'"