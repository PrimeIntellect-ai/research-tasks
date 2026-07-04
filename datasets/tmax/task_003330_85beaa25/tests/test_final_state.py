# test_final_state.py
import os
import subprocess
import random
import pytest

def test_eval_primer_equivalence():
    agent_path = "/home/user/eval_primer"
    oracle_path = "/app/oracle_eval_primer"

    assert os.path.exists(agent_path), f"Agent executable {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."

    assert os.path.exists(oracle_path), f"Oracle executable {oracle_path} is missing."
    assert os.access(oracle_path, os.X_OK), f"Oracle executable {oracle_path} is not executable."

    random.seed(42)
    chars = "ACGT"

    for _ in range(100):
        length = random.randint(10, 50)
        seq = "".join(random.choice(chars) for _ in range(length))

        agent_result = subprocess.run([agent_path, seq], capture_output=True, text=True)
        oracle_result = subprocess.run([oracle_path, seq], capture_output=True, text=True)

        assert agent_result.returncode == 0, f"Agent program failed on input {seq} with stderr: {agent_result.stderr}"
        assert oracle_result.returncode == 0, f"Oracle program failed on input {seq} with stderr: {oracle_result.stderr}"

        agent_output = agent_result.stdout.strip()
        oracle_output = oracle_result.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on input {seq}.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )