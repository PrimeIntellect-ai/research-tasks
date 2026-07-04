# test_final_state.py

import os
import math
import pytest

def test_roots_accuracy():
    agent_file = "/home/user/roots.txt"
    truth_file = "/tmp/truth_roots.txt"

    assert os.path.exists(agent_file), f"Agent output file not found: {agent_file}"
    assert os.path.exists(truth_file), f"Truth output file not found: {truth_file}"

    with open(agent_file, "r") as f:
        agent_lines = [line.strip() for line in f if line.strip()]

    with open(truth_file, "r") as f:
        truth_lines = [line.strip() for line in f if line.strip()]

    assert len(agent_lines) == 1000, f"Expected 1000 lines in {agent_file}, got {len(agent_lines)}"
    assert len(truth_lines) == 1000, f"Expected 1000 lines in {truth_file}, got {len(truth_lines)}"

    max_err = 0.0
    for i, (agent_val, truth_val) in enumerate(zip(agent_lines, truth_lines)):
        if agent_val == "NaN" or truth_val == "NaN":
            if agent_val != truth_val:
                max_err = max(max_err, 999.0)
        else:
            try:
                a_float = float(agent_val)
                t_float = float(truth_val)
                err = abs(a_float - t_float)
                max_err = max(max_err, err)
            except ValueError:
                max_err = max(max_err, 999.0)

    assert max_err <= 1e-5, f"Maximum Absolute Error {max_err} exceeds threshold 1e-5. The calculated roots are not accurate enough."