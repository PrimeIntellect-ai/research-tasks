# test_final_state.py

import os
import subprocess
import pytest

def test_optimizer_go_exists():
    """Check if the Go source code was created."""
    go_path = "/home/user/optimizer.go"
    assert os.path.isfile(go_path), f"Go source code missing at {go_path}"

def test_optimal_plan_exists():
    """Check if the optimal plan output file was created."""
    plan_path = "/home/user/optimal_plan.txt"
    assert os.path.isfile(plan_path), f"Optimal plan missing at {plan_path}"

def test_optimal_plan_cost():
    """Evaluate the optimal plan using the restore_eval binary and check the cost."""
    plan_path = "/home/user/optimal_plan.txt"
    eval_bin = "/app/restore_eval"

    assert os.path.isfile(plan_path), f"Plan file missing at {plan_path}"
    assert os.path.isfile(eval_bin), f"Evaluator binary missing at {eval_bin}"

    try:
        result = subprocess.run(
            [eval_bin, plan_path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Evaluator binary failed with exit code {e.returncode}. Output: {e.stdout}\nError: {e.stderr}")

    output = result.stdout.strip()

    try:
        cost = float(output)
    except ValueError:
        pytest.fail(f"Evaluator did not output a valid float. Output was: {output}")

    threshold = 150000.0
    assert cost <= threshold, f"Cost {cost} is too high. It must be <= {threshold}"