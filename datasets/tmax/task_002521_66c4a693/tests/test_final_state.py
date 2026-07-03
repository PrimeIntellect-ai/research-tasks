# test_final_state.py

import os
import subprocess
import random
import pytest

def test_optimized_engine_exists():
    agent_script = "/home/user/optimized_cost_engine.py"
    assert os.path.exists(agent_script), f"Agent's script {agent_script} does not exist."
    assert os.path.isfile(agent_script), f"{agent_script} is not a file."

def test_fuzz_equivalence():
    oracle_bin = "/app/legacy_join_cost_engine"
    agent_script = "/home/user/optimized_cost_engine.py"

    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} missing."
    assert os.path.exists(agent_script), f"Agent script {agent_script} missing."

    random.seed(42)

    num_iterations = 1000
    for _ in range(num_iterations):
        src_id = random.randint(1, 100)
        dst_id = random.randint(1, 100)

        # Run oracle
        oracle_cmd = [oracle_bin, str(src_id), str(dst_id)]
        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {src_id} {dst_id}: {e.stderr}")

        # Run agent
        agent_cmd = ["python3", agent_script, str(src_id), str(dst_id)]
        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True)
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {src_id} {dst_id}: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Mismatch on inputs src_table_id={src_id}, dst_table_id={dst_id}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )