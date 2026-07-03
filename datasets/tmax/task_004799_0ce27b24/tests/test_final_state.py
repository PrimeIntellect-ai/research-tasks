# test_final_state.py

import os
import subprocess
import time
import tempfile
import pytest

AGENT_BINARY = "/home/user/fast_resolver"
LEGACY_BINARY = "/app/legacy_resolver"

def generate_dense_dag(filepath, num_nodes=22):
    """Generate a densely connected DAG to force exponential time on naive algorithms."""
    with open(filepath, 'w') as f:
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                f.write(f"node{i} node{j}\n")

def test_binary_exists_and_executable():
    assert os.path.isfile(AGENT_BINARY), f"Expected binary not found at {AGENT_BINARY}"
    assert os.access(AGENT_BINARY, os.X_OK), f"Binary at {AGENT_BINARY} is not executable"

def test_binary_is_statically_linked():
    result = subprocess.run(["file", AGENT_BINARY], capture_output=True, text=True)
    assert "statically linked" in result.stdout.lower(), f"Binary is not statically linked: {result.stdout}"

def test_performance_and_correctness():
    with tempfile.TemporaryDirectory() as tmpdir:
        eval_file = os.path.join(tmpdir, "eval_deps.txt")
        generate_dense_dag(eval_file, num_nodes=22)

        # Run legacy binary
        start_legacy = time.time()
        legacy_proc = subprocess.run([LEGACY_BINARY, eval_file], capture_output=True, text=True)
        time_legacy = time.time() - start_legacy

        assert legacy_proc.returncode == 0, "Legacy binary failed on evaluation graph"
        legacy_output = legacy_proc.stdout.strip()

        # Run agent binary
        start_agent = time.time()
        agent_proc = subprocess.run([AGENT_BINARY, eval_file], capture_output=True, text=True)
        time_agent = time.time() - start_agent

        assert agent_proc.returncode == 0, "Agent binary failed (non-zero exit code) on evaluation graph"
        agent_output = agent_proc.stdout.strip()

        # Correctness
        assert agent_output == legacy_output, f"Output mismatch. Legacy: {legacy_output}, Agent: {agent_output}"

        # Performance
        speedup = time_legacy / max(time_agent, 1e-6)
        assert speedup >= 10.0, f"Speedup threshold not met. Speedup: {speedup:.2f}x (Legacy: {time_legacy:.4f}s, Agent: {time_agent:.4f}s)"

def test_cycle_detection():
    with tempfile.TemporaryDirectory() as tmpdir:
        cycle_file = os.path.join(tmpdir, "cycle_deps.txt")
        with open(cycle_file, 'w') as f:
            f.write("A B\n")
            f.write("B C\n")
            f.write("C A\n")

        agent_proc = subprocess.run([AGENT_BINARY, cycle_file], capture_output=True, text=True)

        assert agent_proc.returncode == 1, "Agent binary must exit with status code 1 on cycle"
        assert agent_proc.stdout.strip() == "CYCLE", "Agent binary must print exactly 'CYCLE' to stdout on cycle"