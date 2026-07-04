# test_final_state.py

import os
import pytest

def test_sim_model_executable_exists():
    path = "/home/user/sim_model"
    assert os.path.isfile(path), f"Executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_min_config_txt():
    path = "/home/user/min_config.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in min_config.txt, found {len(lines)}."

    assert "ALPHA=0.9" in lines, "min_config.txt is missing 'ALPHA=0.9'."
    assert "BETA=0.1" in lines, "min_config.txt is missing 'BETA=0.1'."

def test_fixed_config_txt():
    path = "/home/user/fixed_config.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 lines in fixed_config.txt, found {len(lines)}."

    assert "BETA=0.5" in lines, "fixed_config.txt is missing 'BETA=0.5' or it is incorrectly formatted."
    assert "ALPHA=0.9" in lines, "fixed_config.txt is missing 'ALPHA=0.9'."

    # Check that BETA=0.1 is no longer present
    assert "BETA=0.1" not in lines, "fixed_config.txt should not contain 'BETA=0.1'."

    # Check for presence of some other original lines to ensure it's a copy
    expected_other_lines = [
        "GAMMA=0.5",
        "DELTA=0.4",
        "EPSILON=0.1",
        "ZETA=0.2",
        "ETA=0.3",
        "THETA=0.8",
        "IOTA=0.9",
        "KAPPA=1.0"
    ]
    for line in expected_other_lines:
        assert line in lines, f"fixed_config.txt is missing original line '{line}'."