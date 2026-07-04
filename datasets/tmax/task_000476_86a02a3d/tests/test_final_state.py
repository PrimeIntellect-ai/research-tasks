# test_final_state.py
import os
import pytest

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "/home/user/solution.txt is missing."

def test_config_file_exists():
    assert os.path.isfile("/home/user/sim_engine/config.txt"), "/home/user/sim_engine/config.txt is missing."

def test_solution_matches_truth():
    truth_path = "/home/user/.truth.txt"
    solution_path = "/home/user/solution.txt"

    assert os.path.isfile(truth_path), "Truth file missing from system."
    assert os.path.isfile(solution_path), "Solution file missing."

    with open(truth_path, "r") as f:
        truth_lines = [line.strip() for line in f if line.strip()]

    with open(solution_path, "r") as f:
        solution_lines = [line.strip() for line in f if line.strip()]

    assert len(solution_lines) == len(truth_lines), f"Solution file has {len(solution_lines)} lines, expected {len(truth_lines)}."

    for i, (t_line, s_line) in enumerate(zip(truth_lines, solution_lines)):
        assert s_line == t_line, f"Mismatch on line {i+1} of solution.txt: expected '{t_line}', got '{s_line}'."

def test_config_content():
    truth_path = "/home/user/.truth.txt"
    config_path = "/home/user/sim_engine/config.txt"

    assert os.path.isfile(truth_path), "Truth file missing from system."
    assert os.path.isfile(config_path), "config.txt is missing."

    with open(truth_path, "r") as f:
        coeff = None
        for line in f:
            if line.startswith("COEFFICIENT:"):
                coeff = line.split(":", 1)[1].strip()
                break

    assert coeff is not None, "Could not find COEFFICIENT in truth file."

    with open(config_path, "r") as f:
        config_content = f.read().strip()

    assert config_content == coeff, f"config.txt content '{config_content}' does not match expected coefficient '{coeff}'."