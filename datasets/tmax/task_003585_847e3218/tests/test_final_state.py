# test_final_state.py

import os
import time
import subprocess
import random
import pytest

def generate_expression_and_value(depth=0):
    if depth > 2:
        n = random.randint(1, 20)
        return str(n), n

    op = random.choice(['+', '-', '*', '/', 'SUM_SQ', 'MOD'])
    s1, v1 = generate_expression_and_value(depth + 1)
    s2, v2 = generate_expression_and_value(depth + 1)

    if op == '+':
        return f"({s1} + {s2})", v1 + v2
    elif op == '-':
        return f"({s1} - {s2})", v1 - v2
    elif op == '*':
        return f"({s1} * {s2})", v1 * v2
    elif op == '/':
        if v2 == 0:
            v2 = 1
            s2 = "1"
        # Integer division matching C semantics (truncate towards zero)
        # Python's // is floor division. 
        res = int(v1 / v2)
        return f"({s1} / {s2})", res
    elif op == 'SUM_SQ':
        return f"SUM_SQ({s1}, {s2})", v1*v1 + v2*v2
    elif op == 'MOD':
        if v2 == 0:
            v2 = 1
            s2 = "1"
        # C modulo semantics
        import math
        res = math.fmod(v1, v2)
        return f"MOD({s1}, {s2})", int(res)

def test_fast_eval_performance_and_accuracy():
    fast_eval_path = "/home/user/fast_eval.py"
    assert os.path.exists(fast_eval_path), f"Python script missing at {fast_eval_path}"

    hidden_input = "/tmp/hidden_eval.txt"
    hidden_output = "/tmp/fast_out.txt"

    random.seed(42)
    expected_results = []

    with open(hidden_input, "w") as f:
        for _ in range(10000):
            expr, val = generate_expression_and_value()
            f.write(f"{expr}\n")
            expected_results.append(val)

    start_time = time.time()
    result = subprocess.run(
        ["python3", fast_eval_path, hidden_input, hidden_output],
        capture_output=True,
        text=True
    )
    end_time = time.time()

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    elapsed = end_time - start_time
    assert elapsed <= 1.0, f"Execution time {elapsed:.2f}s exceeded threshold of 1.0s"

    assert os.path.exists(hidden_output), f"Output file missing at {hidden_output}"

    with open(hidden_output, "r") as f:
        actual_results = [line.strip() for line in f if line.strip()]

    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} outputs, got {len(actual_results)}"

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert str(actual) == str(expected), f"Mismatch at line {i+1}: expected {expected}, got {actual}"

def test_final_results_exist():
    final_expr = "/home/user/data/final_expressions.txt"
    results = "/home/user/data/results.txt"

    assert os.path.exists(final_expr), f"Patched file missing at {final_expr}"
    assert os.path.exists(results), f"Results file missing at {results}"