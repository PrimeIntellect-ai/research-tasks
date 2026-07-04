# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle"
AGENT_PATH = "/home/user/audit"
NUM_TESTS = 1000

def generate_input():
    T = random.randint(10, 500)
    lines = [str(T)]
    for _ in range(T):
        u = random.randint(1, 200)
        v = random.randint(1, 200)
        amount = random.randint(1000, 20000)
        lines.append(f"{u} {v} {amount}")

    Q = random.randint(5, 50)
    lines.append(str(Q))
    for _ in range(Q):
        u = random.randint(1, 200)
        v = random.randint(1, 200)
        lines.append(f"{u} {v}")

    return "\n".join(lines) + "\n"

def test_audit_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary {AGENT_PATH} does not exist"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} does not exist"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        test_input = generate_input()

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on test {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on test {i}.")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on test {i}.\nInput:\n{test_input}")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent program crashed on test {i} with return code {agent_proc.returncode}.\nStderr: {agent_proc.stderr}\nInput:\n{test_input}")

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on test {i}!\n"
                f"Input:\n{test_input}\n"
                f"Expected (Oracle):\n{oracle_output}\n"
                f"Got (Agent):\n{agent_output}"
            )