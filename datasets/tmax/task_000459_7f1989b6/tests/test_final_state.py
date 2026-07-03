# test_final_state.py

import os
import time
import subprocess
import pytest

def test_backend_socket_exists():
    sock_path = "/home/user/run/backend.sock"
    assert os.path.exists(sock_path), f"Backend socket not found at {sock_path}. Gunicorn not started correctly or configuration not fixed."

def test_fast_analyzer_exists_and_executable():
    agent_script = "/home/user/fast_analyzer.sh"
    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."

def test_fast_analyzer_correctness_and_speedup():
    agent_script = "/home/user/fast_analyzer.sh"
    baseline_script = "/app/slow_analyzer.sh"

    # Measure baseline
    t0 = time.time()
    try:
        base_out = subprocess.check_output(baseline_script, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Baseline script {baseline_script} failed to run: {e}")
    base_time = time.time() - t0

    # Measure agent
    t0 = time.time()
    try:
        agent_out = subprocess.check_output(agent_script, shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script {agent_script} failed to run: {e}")
    agent_time = time.time() - t0

    # Correctness check
    assert base_out == agent_out, f"Output mismatch. Baseline produced '{base_out}', Agent produced '{agent_out}'."

    # Speedup check
    speedup = base_time / agent_time if agent_time > 0 else float('inf')
    assert speedup >= 10.0, f"Speedup {speedup:.2f}x is below threshold 10.0x. Agent time: {agent_time:.4f}s, Baseline time: {base_time:.4f}s."