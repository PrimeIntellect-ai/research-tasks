# test_final_state.py

import os
import pytest

def test_runner_c_exists():
    assert os.path.isfile("/home/user/artifacts/runner.c"), "runner.c is missing. You must write the C program."

def test_result_log_exists():
    assert os.path.isfile("/home/user/artifacts/result.log"), "result.log is missing. Your program must generate this file."

def test_result_log_content():
    expected_order = "Order: tree, node, graph, edge, vertex"
    expected_state = "Final State: 0xAF250DAF"

    with open("/home/user/artifacts/result.log", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "result.log must contain at least two lines of output."

    assert lines[0] == expected_order, f"The first line of result.log is incorrect. Expected '{expected_order}', got '{lines[0]}'."
    assert lines[1] == expected_state, f"The second line of result.log is incorrect. Expected '{expected_state}', got '{lines[1]}'."