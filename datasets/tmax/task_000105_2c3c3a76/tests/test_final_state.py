# test_final_state.py
import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    agent_path = "/home/user/project/engine"
    oracle_path = "/opt/oracle/engine"

    assert os.path.isfile(agent_path), f"Agent binary {agent_path} does not exist. Did you compile the project?"
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} does not exist."
    assert os.access(oracle_path, os.X_OK), f"Oracle binary {oracle_path} is not executable."

    random.seed(42)
    inputs = [random.randint(1, 1000000) for _ in range(50)]

    for val in inputs:
        val_str = str(val)

        agent_res = subprocess.run([agent_path, val_str], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent binary failed on input {val_str} with stderr: {agent_res.stderr}"

        oracle_res = subprocess.run([oracle_path, val_str], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle binary failed on input {val_str}"

        agent_out = agent_res.stdout.strip()
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input {val_str}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}\n"
            "The constants extracted from the image might be incorrect or the build is outdated."
        )