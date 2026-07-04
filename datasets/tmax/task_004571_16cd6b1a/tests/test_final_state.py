# test_final_state.py

import os
import pytest

def test_result_count():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file missing: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        agent_val = int(content)
    except ValueError:
        pytest.fail(f"Result file does not contain a valid integer. Found: '{content}'")

    target_value = 14
    error = abs(agent_val - target_value)

    assert error <= 0, f"Metric threshold failed: Expected exactly {target_value} frames, but found {agent_val}. Error: {error} > 0"

def test_script_exists():
    script_path = "/home/user/run_e2e.sh"
    assert os.path.isfile(script_path), f"Bash script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Bash script is not executable: {script_path}"

def test_c_source_exists():
    c_path = "/home/user/src/analyze_frame.c"
    assert os.path.isfile(c_path), f"C source missing: {c_path}"