# test_final_state.py

import os
import pytest

def test_aggregator_executable_exists():
    executable_path = "/home/user/log_tool/aggregator"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_timeline_txt_exists():
    assert os.path.isfile("/home/user/timeline.txt"), "Output file /home/user/timeline.txt is missing."

def test_timeline_txt_content():
    expected_lines = [
        "1620000001 Service B initialized",
        "1620000005 Service A started",
        "1620000008 Service B waiting",
        "1620000010 Service A connecting",
        "1620000015 Service B error",
        "1620000020 Service A connected"
    ]

    with open("/home/user/timeline.txt", "r") as f:
        actual_lines = f.readlines()

    actual_lines_clean = [line.strip() for line in actual_lines if line.strip()]

    assert actual_lines_clean == expected_lines, (
        f"Timeline content is incorrect.\nExpected:\n{expected_lines}\nGot:\n{actual_lines_clean}"
    )