# test_final_state.py

import os
import sys
import time
import subprocess
import pytest

def test_fast_extract_exists():
    path = "/home/user/fast_extract.py"
    assert os.path.isfile(path), f"Expected optimized script missing at {path}"

def test_speedup_and_correctness():
    baseline_path = "/home/user/baseline.py"
    agent_path = "/home/user/fast_extract.py"
    output_path = "/home/user/filtered_backup.fc"

    assert os.path.isfile(baseline_path), f"Baseline script missing at {baseline_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    # Remove the output file if it exists to ensure we generate a fresh one
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run baseline
    t0 = time.time()
    try:
        subprocess.run([sys.executable, baseline_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Baseline script failed to run:\n{e.stderr}")
    base_time = time.time() - t0

    # Ensure baseline created the output and remove it
    assert os.path.exists(output_path), "Baseline script did not create the output file"
    os.remove(output_path)

    # Run agent script
    t1 = time.time()
    try:
        subprocess.run([sys.executable, agent_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed to run:\n{e.stderr}")
    agent_time = time.time() - t1

    assert agent_time > 0, "Agent script executed in 0 seconds, which is invalid."
    speedup = base_time / agent_time

    assert speedup >= 3.0, f"Speedup {speedup:.2f}x is less than the 3.0x threshold (Base: {base_time:.2f}s, Agent: {agent_time:.2f}s)"

    # Verify correctness of output
    assert os.path.exists(output_path), f"Agent script did not create the output file at {output_path}"

    try:
        import fastchunker
    except ImportError:
        pytest.fail("Failed to import 'fastchunker'. Ensure the package is fixed and installed in the environment.")

    try:
        reader = fastchunker.ChunkReader(output_path)
        data = reader.read_all()
    except Exception as e:
        pytest.fail(f"Failed to read output file with fastchunker.ChunkReader: {e}")

    assert "SERVER_ID: srv_0" in data, "Output data is missing expected 'SERVER_ID: srv_0' content."
    assert "[ERROR]" in data, "Output data is missing expected '[ERROR]' log content."