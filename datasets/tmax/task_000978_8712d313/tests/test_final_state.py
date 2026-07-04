# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/logistic_sim"
AGENT_PATH = "/home/user/py_sim.py"
N_ITERATIONS = 1000

def test_py_sim_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} does not exist."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable."

    random.seed(42)

    for i in range(N_ITERATIONS):
        y0 = random.uniform(0.1, 10.0)
        r = random.uniform(0.1, 2.0)
        K = random.uniform(10.0, 100.0)
        dt = random.uniform(0.01, 0.5)
        n_steps = random.randint(1, 200)

        args = [f"{y0:.6f}", f"{r:.6f}", f"{K:.6f}", f"{dt:.6f}", str(n_steps)]

        # Run oracle
        oracle_cmd = [ORACLE_PATH] + args
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on args {args}:\n{oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["python3", AGENT_PATH] + args
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on args {args}:\n{agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i+1}.\n"
            f"Arguments: y0={args[0]}, r={args[1]}, K={args[2]}, dt={args[3]}, n_steps={args[4]}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )