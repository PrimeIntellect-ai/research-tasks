# test_final_state.py

import os
import subprocess
import random
import math
import pytest

def generate_expr(depth=0):
    if depth > 3 or random.random() < 0.3:
        return str(random.randint(-100, 100))
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)
    left = generate_expr(depth + 1)
    right = generate_expr(depth + 1)
    if op == '/' and right == '0': right = '1'
    fmt = random.choice(["{} {} {}", "({} {} {})", "{}{}{}", "({}{}{})"])
    return fmt.format(left, op, right)

def test_final_evaluator_exists_and_executable():
    path = "/home/user/final_evaluator"
    assert os.path.exists(path), f"Final evaluator executable not found at {path}"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_evaluator_accuracy():
    agent_bin = "/home/user/final_evaluator"
    oracle_bin = "/app/math_oracle"

    assert os.path.exists(agent_bin), f"Agent binary missing: {agent_bin}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    correct = 0
    total = 1000
    random.seed(42)  # For reproducibility

    for _ in range(total):
        expr = generate_expr()
        try:
            ref_out = subprocess.check_output([oracle_bin, expr], stderr=subprocess.DEVNULL).decode().strip()
            agent_out = subprocess.check_output([agent_bin, expr], stderr=subprocess.DEVNULL, timeout=1).decode().strip()

            if math.isclose(float(ref_out), float(agent_out), rel_tol=1e-6, abs_tol=1e-6):
                correct += 1
        except Exception:
            pass

    accuracy = correct / total
    assert accuracy >= 0.99, f"Accuracy {accuracy} is below the threshold of 0.99"