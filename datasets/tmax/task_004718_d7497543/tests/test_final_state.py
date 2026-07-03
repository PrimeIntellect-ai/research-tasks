# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/restore_planner.py"
ORACLE_BINARY = "/app/oracle_planner"
NUM_ITERATIONS = 100
NODE_MIN = 1
NODE_MAX = 500

def test_restore_planner_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary {ORACLE_BINARY} missing."
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary {ORACLE_BINARY} is not executable."

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        source_id = random.randint(NODE_MIN, NODE_MAX)
        target_id = random.randint(NODE_MIN, NODE_MAX)

        # Run Oracle
        oracle_cmd = [ORACLE_BINARY, str(source_id), str(target_id)]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on {source_id} -> {target_id} with error: {oracle_proc.stderr}"
        oracle_output = oracle_proc.stdout.strip()

        # Run Agent Script
        agent_cmd = ["python3", AGENT_SCRIPT, str(source_id), str(target_id)]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on {source_id} -> {target_id} with error: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i+1} for source_id={source_id}, target_id={target_id}.\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )