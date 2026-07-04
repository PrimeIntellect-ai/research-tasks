# test_final_state.py

import os
import time
import subprocess
import pytest

def test_fast_verifier_speedup():
    script_path = '/home/user/fast_verifier.py'
    binary_path = '/app/chunk_verifier'
    db_path = '/home/user/backup_metadata.db'

    assert os.path.exists(script_path), f"Agent script missing at {script_path}"
    assert os.path.exists(binary_path), f"Binary missing at {binary_path}"
    assert os.path.exists(db_path), f"Database missing at {db_path}"

    # Run baseline
    start_binary = time.time()
    try:
        binary_out = subprocess.check_output([binary_path, db_path]).decode().strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Binary execution failed: {e}")
    binary_time = time.time() - start_binary

    # Run agent script
    start_agent = time.time()
    try:
        agent_out = subprocess.check_output(['python3', script_path]).decode().strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script execution failed: {e}")
    agent_time = time.time() - start_agent

    assert binary_out == agent_out, f"Output mismatch: binary output '{binary_out}' != agent output '{agent_out}'"

    speedup = binary_time / agent_time
    assert speedup >= 5.0, f"Speedup too low: {speedup:.2f}x (needs >= 5.0x). Binary time: {binary_time:.4f}s, Agent time: {agent_time:.4f}s"