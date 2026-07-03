# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/sensor_calc_oracle"
AGENT_PATH = "/home/user/sensor_calc"
NUM_TESTS = 1000

def generate_test_case():
    k = random.randint(2, 50)
    is_clustered = random.random() < 0.5

    args = []
    if is_clustered:
        base = 1e8
        for _ in range(k):
            val = base + random.uniform(-1.0, 1.0)
            args.append(f"{val:.6f}")
    else:
        for _ in range(k):
            val = random.uniform(-1000.0, 1000.0)
            args.append(f"{val:.6f}")

    return args

def test_sensor_calc_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent's executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent's file at {AGENT_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        args = generate_test_case()

        oracle_cmd = [ORACLE_PATH] + args
        agent_cmd = [AGENT_PATH] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_res.returncode == oracle_res.returncode, (
            f"Test case {i+1} failed.\n"
            f"Arguments: {' '.join(args)}\n"
            f"Oracle return code: {oracle_res.returncode}\n"
            f"Agent return code: {agent_res.returncode}\n"
        )

        assert agent_res.stdout == oracle_res.stdout, (
            f"Test case {i+1} failed.\n"
            f"Arguments: {' '.join(args)}\n"
            f"Oracle stdout:\n{oracle_res.stdout}\n"
            f"Agent stdout:\n{agent_res.stdout}\n"
        )