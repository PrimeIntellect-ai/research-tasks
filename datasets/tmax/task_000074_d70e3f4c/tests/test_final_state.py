# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_process"
    agent_path = "/home/user/process.sh"

    assert os.path.isfile(agent_path), f"Agent script not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable"

    assert os.path.isfile(oracle_path), f"Oracle script not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle script {oracle_path} is not executable"

    random.seed(42)
    ops = ["add", "sub", "mul"]

    for _ in range(1000):
        val1 = random.randint(0, 9999)
        val2 = random.randint(0, 9999)
        op = random.choice(ops)

        query = f"val1={val1}&val2={val2}&op={op}"

        oracle_res = subprocess.run([oracle_path, query], capture_output=True, text=True)
        agent_res = subprocess.run([agent_path, query], capture_output=True, text=True)

        assert oracle_res.returncode == agent_res.returncode, (
            f"Return code mismatch on input '{query}': "
            f"oracle={oracle_res.returncode}, agent={agent_res.returncode}\n"
            f"Agent stderr: {agent_res.stderr}"
        )

        assert oracle_res.stdout == agent_res.stdout, (
            f"Output mismatch on input '{query}'.\n"
            f"Expected (Oracle):\n{oracle_res.stdout}\n"
            f"Got (Agent):\n{agent_res.stdout}\n"
            f"Agent stderr: {agent_res.stderr}"
        )