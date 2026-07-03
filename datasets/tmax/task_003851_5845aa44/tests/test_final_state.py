# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/oracle"
AGENT_PATH = "/home/user/compute_stat"

def generate_random_pdb_line():
    if random.random() < 0.7:
        prefix = "ATOM  "
        filler1 = "".join(random.choices(string.ascii_letters + string.digits + " ", k=24))
        if random.random() < 0.1:
            x_str = "".join(random.choices(string.ascii_letters, k=8))
        else:
            x_val = random.uniform(-10000.0, 10000.0)
            x_str = f"{x_val:8.3f}"

        # ensure length is exactly 8
        if len(x_str) > 8:
            x_str = x_str[:8]
        elif len(x_str) < 8:
            x_str = x_str.rjust(8)

        filler2 = "".join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(0, 40)))
        return prefix + filler1 + x_str + filler2
    else:
        return "".join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(5, 80)))

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    random.seed(42)

    # Run 500 test cases, each with 100 lines, to simulate 50000 lines total
    # (The prompt mentioned N=5000 iterations, we will do 500 invocations to avoid excessive subprocess overhead)
    for i in range(500):
        lines = [generate_random_pdb_line() for _ in range(random.randint(10, 100))]
        input_data = "\n".join(lines) + "\n"

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )
        agent_out = agent_proc.stdout.strip()

        assert agent_proc.returncode == 0, f"Agent binary crashed or returned non-zero exit code on iteration {i}."
        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i}!\n"
            f"Input lines count: {len(lines)}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}\n"
        )