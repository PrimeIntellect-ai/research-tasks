# test_final_state.py

import os
import time
import subprocess
import pytest

def test_optimized_db_exists():
    path = "/home/user/optimized.db"
    assert os.path.exists(path), f"Optimized database {path} is missing. Did you create it?"
    assert os.path.isfile(path), f"{path} is not a file."

def test_compute_path_script_exists():
    path = "/home/user/compute_path.sh"
    assert os.path.exists(path), f"Script {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_performance_and_correctness():
    agent_script = "/home/user/compute_path.sh"
    ref_script = "/app/ref_slow.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."
    assert os.path.exists(ref_script), f"Reference script {ref_script} not found."

    # Run Agent script
    start = time.time()
    agent_res = subprocess.run(["bash", agent_script], capture_output=True, text=True)
    agent_time = time.time() - start

    assert agent_res.returncode == 0, f"Agent script failed with error: {agent_res.stderr}"

    # Run Reference script
    start = time.time()
    ref_res = subprocess.run(["python3", ref_script], capture_output=True, text=True)
    ref_time = time.time() - start

    assert ref_res.returncode == 0, f"Reference script failed with error: {ref_res.stderr}"

    try:
        agent_cost = int(agent_res.stdout.strip())
    except ValueError:
        pytest.fail(f"Agent script output is not an integer: {agent_res.stdout.strip()}")

    try:
        ref_cost = int(ref_res.stdout.strip())
    except ValueError:
        pytest.fail(f"Reference script output is not an integer: {ref_res.stdout.strip()}")

    assert agent_cost == 142, f"Agent script output {agent_cost} does not match the correct shortest path cost 142."
    assert ref_cost == 142, f"Reference script output {ref_cost} does not match 142."

    speedup = ref_time / agent_time
    assert speedup >= 5.0, f"Speedup {speedup:.2f}x is less than threshold 5.0x (Agent time: {agent_time:.4f}s, Ref time: {ref_time:.4f}s)"