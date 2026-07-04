# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    N = random.randint(10, 500)
    E = random.randint(20, 2000)

    lines = [f"{N} {E}"]

    for _ in range(E):
        u = random.randint(0, N - 1)
        v = random.randint(0, N - 1)
        while v == u and N > 1:
            v = random.randint(0, N - 1)
        R = random.randint(1, 5)
        lines.append(f"{u} {v} {R}")

    Q = 100
    lines.append(f"{Q}")

    for _ in range(Q):
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        lines.append(f"{x} {y}")

    return "\n".join(lines) + "\n"

def test_checker_fuzz_equivalence():
    agent_prog = "/home/user/checker"
    oracle_prog = "/opt/oracle/checker_oracle"

    assert os.path.isfile(agent_prog), f"Agent program {agent_prog} does not exist."
    assert os.access(agent_prog, os.X_OK), f"Agent program {agent_prog} is not executable."

    assert os.path.isfile(oracle_prog), f"Oracle program {oracle_prog} does not exist."
    assert os.access(oracle_prog, os.X_OK), f"Oracle program {oracle_prog} is not executable."

    num_iterations = 100

    for i in range(num_iterations):
        input_data = generate_fuzz_input(seed=42 + i)

        try:
            agent_proc = subprocess.run(
                [agent_prog],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on iteration {i}")

        try:
            oracle_proc = subprocess.run(
                [oracle_prog],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle program timed out on iteration {i}")

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Input:\n{input_data[:200]}...\n"
                f"Expected (Oracle):\n{oracle_out[:200]}...\n"
                f"Got (Agent):\n{agent_out[:200]}...\n"
            )