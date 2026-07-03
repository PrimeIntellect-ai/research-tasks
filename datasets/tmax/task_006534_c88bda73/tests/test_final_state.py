# test_final_state.py

import os
import subprocess
import math

def test_cargo_test_passes():
    """Verify that the Rust code was fixed and cargo test passes deterministically."""
    project_dir = "/home/user/motif_scorer"
    assert os.path.isdir(project_dir), "Project directory is missing."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\n{result.stdout}\n{result.stderr}"

def test_best_weights_file():
    """Verify that best_weights.txt exists and contains valid weights summing to 1."""
    filepath = "/home/user/best_weights.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 4, f"Expected 4 comma-separated values in {filepath}, found {len(parts)}."

    try:
        weights = [float(w) for w in parts]
    except ValueError:
        raise AssertionError(f"Values in {filepath} are not valid floats: {content}")

    for w in weights:
        assert w >= 0.0, f"Weights must be non-negative, found {w}."

    total_weight = sum(weights)
    assert math.isclose(total_weight, 1.0, rel_tol=1e-3, abs_tol=1e-3), \
        f"Weights must sum to 1.0, but sum is {total_weight}."

def test_max_score_file():
    """Verify that max_score.txt exists and contains a valid number."""
    filepath = "/home/user/max_score.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    try:
        score = float(content)
    except ValueError:
        raise AssertionError(f"Content of {filepath} is not a valid float: {content}")

def test_optimization_trace_plot():
    """Verify that the optimization trace plot exists."""
    filepath = "/home/user/optimization_trace.png"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    assert os.path.getsize(filepath) > 0, f"{filepath} is empty."