# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    """
    Fuzz-equivalence test to ensure the agent's C++ program exactly matches
    the behavior of the reference oracle on 1000 random inputs.
    """
    oracle_path = "/app/oracle_polyfit"
    agent_path = "/home/user/poly_fit"

    assert os.path.exists(oracle_path), f"Oracle executable missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle executable at {oracle_path} is not executable"

    assert os.path.exists(agent_path), f"Agent executable missing at {agent_path}. Did you compile it?"
    assert os.access(agent_path, os.X_OK), f"Agent executable at {agent_path} is not executable."

    random.seed(42)
    N = 1000
    p = 8191

    for _ in range(N):
        # Generate 3 distinct x values modulo p
        xs = random.sample(range(p), 3)
        # Generate 3 random y values modulo p
        ys = [random.randint(0, p - 1) for _ in range(3)]

        args = [
            str(xs[0]), str(ys[0]),
            str(xs[1]), str(ys[1]),
            str(xs[2]), str(ys[2])
        ]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {' '.join(args)}"
        assert agent_proc.returncode == 0, (
            f"Agent program returned non-zero exit code on input: {' '.join(args)}\n"
            f"Stderr: {agent_proc.stderr}"
        )

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: {' '.join(args)}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )