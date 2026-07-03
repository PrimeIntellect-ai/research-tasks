# test_final_state.py

import os
import pytest

def test_planner_script_exists():
    filepath = "/home/user/planner.py"
    assert os.path.exists(filepath), f"Missing script file: {filepath}"
    assert os.path.isfile(filepath), f"{filepath} should be a file"

def test_report_txt_exists_and_correct():
    filepath = "/home/user/report.txt"
    assert os.path.exists(filepath), f"Missing report file: {filepath}"
    assert os.path.isfile(filepath), f"{filepath} should be a file"

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_content = "Conflict: requested 10.10.10.128/25 overlaps with metrics_net (10.10.10.0/24)"

    assert content == expected_content, (
        f"Incorrect content in {filepath}. "
        f"Expected: '{expected_content}', but got: '{content}'"
    )