# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_query"
    agent_script = "/home/user/dataset_query.py"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)

    for i in range(50):
        dataset_id = random.randint(1, 50)
        max_depth = random.randint(1, 4)
        limit = random.randint(5, 20)
        offset = random.randint(0, 10)

        args = [
            "--dataset-id", str(dataset_id),
            "--max-depth", str(max_depth),
            "--limit", str(limit),
            "--offset", str(offset)
        ]

        oracle_cmd = [oracle_path] + args
        agent_cmd = ["python3", agent_script] + args

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {args}: {e.stderr}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
            agent_out = agent_res.stdout.strip()
        except Exception as e:
            pytest.fail(f"Agent script failed to execute on input {args}: {e}")

        assert agent_res.returncode == 0, f"Agent script returned non-zero exit code on input {args}. Stderr: {agent_res.stderr}"
        assert agent_out == oracle_out, f"Mismatch on input {args}.\nExpected (Oracle): {oracle_out}\nGot (Agent): {agent_out}"