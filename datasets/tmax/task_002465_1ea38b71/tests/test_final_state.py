# test_final_state.py

import os
import random
import subprocess
import pytest

def test_agent_executable_exists():
    agent_path = "/home/user/simulate_growth"
    assert os.path.isfile(agent_path), f"Agent executable missing: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent is not executable: {agent_path}"

def test_fuzz_equivalence():
    agent_path = "/home/user/simulate_growth"
    oracle_path = "/app/oracle_simulate_growth"

    assert os.path.isfile(oracle_path), f"Oracle executable missing: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle is not executable: {oracle_path}"

    random.seed(42)
    N = 100

    for _ in range(N):
        L = random.randint(50, 500)
        y0 = round(random.uniform(1.00, 10.00), 2)

        args = [str(L), f"{y0:.2f}"]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on inputs {args}\nStderr: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent failed on inputs {args}\nStderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on inputs L={L}, y0={y0:.2f}:\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Actual (Agent):   {agent_out}"
        )