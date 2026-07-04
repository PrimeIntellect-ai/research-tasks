# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/gelman_rubin_oracle"
AGENT_PATH = "/home/user/gelman_rubin"

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"

    random.seed(42)
    num_tests = 1000

    for i in range(num_tests):
        M = random.randint(2, 5)
        N = random.randint(5, 20)

        args = [str(M), str(N)]
        for _ in range(M * N):
            val = random.uniform(-10.0, 10.0)
            args.append(f"{val:.6f}")

        oracle_cmd = [ORACLE_PATH] + args
        agent_cmd = [AGENT_PATH] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input: {' '.join(args)}"
        oracle_out = oracle_res.stdout.strip()

        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent program failed on input: {' '.join(args)}\nStderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on test {i+1}/{num_tests}!\n"
            f"Input args: {' '.join(args)}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )