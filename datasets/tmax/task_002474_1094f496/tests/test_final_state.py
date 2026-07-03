# test_final_state.py

import os
import time
import subprocess
import pytest

def test_libtinyexpr_compiled():
    so_path = "/app/tinyexpr/libtinyexpr.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not compiled. Make sure to fix the Makefile and build it."

def test_fast_router_exists():
    script_path = "/home/user/fast_router.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_fast_router_performance_and_correctness():
    script_path = "/home/user/fast_router.py"
    requests_path = "/home/user/requests.txt"
    results_path = "/home/user/results.txt"
    baseline_results_path = "/home/user/baseline_results.txt"

    # Ensure baseline results exist
    assert os.path.isfile(baseline_results_path), f"Baseline results missing at {baseline_results_path}."

    # Remove previous results if any
    if os.path.exists(results_path):
        os.remove(results_path)

    # Run the fast router and measure time
    start = time.time()
    result = subprocess.run(
        ["python3", script_path, requests_path, results_path],
        capture_output=True, text=True
    )
    end = time.time()
    runtime = end - start

    assert result.returncode == 0, f"fast_router.py failed with error:\n{result.stderr}"
    assert os.path.isfile(results_path), f"Output file {results_path} was not created."

    # Check correctness
    with open(results_path, "r") as f1, open(baseline_results_path, "r") as f2:
        actual = [l.strip() for l in f1.readlines()]
        expected = [l.strip() for l in f2.readlines()]

    assert len(actual) == len(expected), f"Output length mismatch: {len(actual)} vs {len(expected)}"

    accuracy = sum(1 for a, b in zip(actual, expected) if a == b) / len(expected)
    assert accuracy == 1.0, f"Accuracy {accuracy:.4f} < 1.0. Outputs do not exactly match the baseline."

    # Check performance metric
    assert runtime <= 1.5, f"Runtime {runtime:.3f}s > 1.5s threshold. The solution is not fast enough."