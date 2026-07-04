# test_final_state.py
import json
import time
import subprocess
import os
import pytest

def test_analyzer_binary_exists():
    path = "/home/user/pipeline/analyzer"
    assert os.path.isfile(path), f"Compiled binary not found at {path}"
    assert os.access(path, os.X_OK), f"Binary at {path} is not executable"

def test_analyzer_execution_and_metrics():
    binary_path = "/home/user/pipeline/analyzer"
    results_path = "/home/user/results.json"

    # Remove results.json if it exists to ensure we are checking the new output
    if os.path.exists(results_path):
        os.remove(results_path)

    start_time = time.time()
    result = subprocess.run([binary_path], capture_output=True, text=True)
    duration = time.time() - start_time

    assert result.returncode == 0, f"Analyzer failed to run. Stderr: {result.stderr}"
    assert duration < 5.0, f"Runtime {duration:.2f}s exceeded 5.0s threshold."

    assert os.path.isfile(results_path), f"Results file not generated at {results_path}"

    try:
        with open(results_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not read or parse {results_path}: {e}")

    assert "kl_divergence_0_vs_299" in data, "Missing 'kl_divergence_0_vs_299' in output JSON"
    assert "max_effective_resistance" in data, "Missing 'max_effective_resistance' in output JSON"
    assert "runtime_seconds" in data, "Missing 'runtime_seconds' in output JSON"

    agent_kl = data["kl_divergence_0_vs_299"]
    truth_kl = 0.4125
    error = abs(agent_kl - truth_kl)

    assert error <= 0.05, f"KL error {error:.4f} > 0.05 threshold (agent: {agent_kl}, truth: {truth_kl})"