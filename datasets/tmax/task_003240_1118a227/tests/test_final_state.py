# test_final_state.py

import os
import subprocess
import time
import pytest

def test_fixed_parser_exists():
    path = "/home/user/fixed_parser"
    assert os.path.exists(path), f"Fixed parser binary {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_fixed_parser_accuracy_and_performance():
    dataset_path = "/hidden_data/telemetry_logs"
    ref_binary = "/app/ref_parser"
    agent_binary = "/home/user/fixed_parser"

    assert os.path.exists(dataset_path), f"Dataset path {dataset_path} does not exist."
    assert os.path.exists(ref_binary), f"Reference binary {ref_binary} does not exist."

    # Run reference
    ref_proc = subprocess.run([ref_binary, dataset_path], capture_output=True, text=True)
    assert ref_proc.returncode == 0, "Reference binary failed to execute."

    ref_output = ref_proc.stdout.strip()
    ref_lines = set(ref_output.split('\n')) if ref_output else set()

    # Run agent
    start_time = time.time()
    try:
        agent_proc = subprocess.run([agent_binary, dataset_path], capture_output=True, text=True, timeout=2.0)
    except subprocess.TimeoutExpired:
        pytest.fail("Timeout expired: fixed_parser took > 2.0s to execute.")

    duration = time.time() - start_time
    assert agent_proc.returncode == 0, f"Fixed parser failed to execute. stderr: {agent_proc.stderr}"

    agent_output = agent_proc.stdout.strip()
    agent_lines = set(agent_output.split('\n')) if agent_output else set()

    if len(ref_lines) == 0:
        accuracy = 0.0 if len(agent_lines) > 0 else 1.0
    else:
        correct = len(ref_lines.intersection(agent_lines))
        accuracy = correct / max(len(ref_lines), len(agent_lines))

    assert duration <= 2.0, f"Execution took too long: {duration:.2f}s (threshold: 2.0s)"
    assert accuracy == 1.0, f"Accuracy is {accuracy:.4f} (threshold: 1.0). Output did not exactly match reference."