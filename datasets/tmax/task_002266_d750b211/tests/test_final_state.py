# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_audit"
    agent_path = "/home/user/audit_cli"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable at {oracle_path}"

    assert os.path.isfile(agent_path), f"Agent program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program not executable at {agent_path}"

    random.seed(42)

    for i in range(100):
        start_account_id = random.randint(1, 1000)
        offset = random.randint(0, 20)
        limit = random.randint(1, 10)

        args = [str(start_account_id), str(offset), str(limit)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on args {args}:\n{oracle_proc.stderr}"

        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent program failed on args {args}:\n{agent_proc.stderr}"

        try:
            oracle_json = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output is not valid JSON on args {args}:\n{oracle_proc.stdout}")

        try:
            agent_json = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output is not valid JSON on args {args}:\n{agent_proc.stdout}")

        assert agent_json == oracle_json, (
            f"Mismatch on args {args}.\n"
            f"Oracle output: {oracle_json}\n"
            f"Agent output: {agent_json}"
        )