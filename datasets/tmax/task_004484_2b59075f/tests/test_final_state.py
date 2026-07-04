# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/audit_repro.py"
    oracle_binary = "/app/legacy_audit"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.exists(oracle_binary), f"Oracle binary {oracle_binary} does not exist."

    random.seed(42)
    fuzz_inputs = [random.randint(1, 1000) for _ in range(100)]

    for user_id in fuzz_inputs:
        oracle_cmd = [oracle_binary, str(user_id)]
        agent_cmd = ["python3", agent_script, str(user_id)]

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {user_id}: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent script failed on input {user_id}: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on user_id={user_id}.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'"
        )