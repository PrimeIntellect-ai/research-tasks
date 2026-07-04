# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_graph.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_result_txt_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you run the script?"

    expected_lines = [
        "Central Node: C",
        "Shortest Path: C->D->E->Node_Z",
        "Total Weight: 6"
    ]

    with open(result_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 3, f"Expected 3 lines in {result_path}, but found {len(content)}."

    for i, expected in enumerate(expected_lines):
        assert content[i].strip() == expected, f"Line {i+1} of {result_path} is incorrect. Expected '{expected}', got '{content[i].strip()}'."