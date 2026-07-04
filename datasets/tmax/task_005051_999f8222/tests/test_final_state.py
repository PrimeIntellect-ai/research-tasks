# test_final_state.py

import os
import time
import subprocess
import pytest

def test_deploy_script_and_speedup():
    script_path = "/home/user/deploy.sh"
    input_file = "/home/user/incoming/routes.txt"
    compiler_path = "/app/mlist_compiler"
    ref_db = "/tmp/reference.db"
    release_id = "test_run_01"

    assert os.path.exists(script_path), f"Deployment script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Deployment script is not executable: {script_path}"

    current_link = "/home/user/deployments/current"
    previous_link = "/home/user/deployments/previous"

    old_current_target = None
    if os.path.islink(current_link):
        old_current_target = os.readlink(current_link)

    # 1. Run reference sequentially
    start_time = time.time()
    try:
        subprocess.run([compiler_path, input_file, ref_db], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Reference compiler failed: {e.stderr.decode('utf-8', errors='ignore')}")
    t_ref = time.time() - start_time

    # 2. Run agent script
    start_time = time.time()
    try:
        subprocess.run([script_path, release_id, input_file], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed: {e.stderr.decode('utf-8', errors='ignore')}")
    t_agent = time.time() - start_time

    speedup = t_ref / t_agent

    # 3. Check symlinks
    assert os.path.islink(current_link), f"{current_link} is not a symlink"
    new_current_target = os.readlink(current_link)
    expected_current_target = f"/home/user/deployments/releases/{release_id}"
    assert new_current_target == expected_current_target, f"Expected current symlink to point to {expected_current_target}, got {new_current_target}"

    if old_current_target is not None:
        assert os.path.islink(previous_link), f"{previous_link} is not a symlink"
        new_previous_target = os.readlink(previous_link)
        assert new_previous_target == old_current_target, f"Expected previous symlink to point to {old_current_target}, got {new_previous_target}"

    # 4. Check file existence and integrity
    agent_db = f"/home/user/deployments/releases/{release_id}/routes.db"
    assert os.path.exists(agent_db), f"Output database missing at {agent_db}"

    with open(ref_db, "rb") as f:
        ref_data = f.read()
    with open(agent_db, "rb") as f:
        agent_data = f.read()

    assert len(ref_data) == len(agent_data), f"Database size mismatch: expected {len(ref_data)} bytes, got {len(agent_data)} bytes"

    # The records are 64-byte blocks. Order might vary due to parallel execution.
    record_size = 64
    ref_blocks = sorted([ref_data[i:i+record_size] for i in range(0, len(ref_data), record_size)])
    agent_blocks = sorted([agent_data[i:i+record_size] for i in range(0, len(agent_data), record_size)])

    assert ref_blocks == agent_blocks, "Database content mismatch after sorting 64-byte records"

    # 5. Check speedup metric
    assert speedup >= 2.8, f"Speedup too low: {speedup:.2f} (T_ref={t_ref:.2f}s, T_agent={t_agent:.2f}s). Expected speedup >= 2.8"