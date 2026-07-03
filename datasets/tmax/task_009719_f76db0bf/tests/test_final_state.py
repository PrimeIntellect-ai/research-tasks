# test_final_state.py

import os
import re

def test_result_file_exists():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Expected result file {result_path} does not exist."

def test_result_file_content():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Expected result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {result_path}, got {len(lines)}."

    # Check max score
    assert "Max Score: 35" in lines[0], f"Expected first line to contain 'Max Score: 35', got '{lines[0]}'."

    # Check root
    # Allow slight variations like '4.0592'
    root_match = re.search(r"Root:\s*([0-9.]+)", lines[1])
    assert root_match is not None, f"Could not parse Root value from second line: '{lines[1]}'."

    root_val = float(root_match.group(1))
    assert abs(root_val - 4.0592) < 1e-4, f"Expected Root to be approximately 4.0592, got {root_val}."