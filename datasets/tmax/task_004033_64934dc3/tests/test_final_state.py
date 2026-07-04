# test_final_state.py

import os
import random
import subprocess
import pytest

def test_extracted_edges_file():
    extracted_path = "/home/user/extracted_edges.txt"
    assert os.path.isfile(extracted_path), f"Extracted edges file missing at {extracted_path}"
    with open(extracted_path, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, "Extracted edges file is empty"

def test_checker_executable():
    checker_path = "/home/user/checker"
    assert os.path.isfile(checker_path), f"Checker binary missing at {checker_path}"
    assert os.access(checker_path, os.X_OK), f"Checker binary at {checker_path} is not executable"

def generate_test_case():
    V = random.randint(10, 500)
    E = random.randint(10, 5000)
    lines = [f"{V} {E}"]
    for _ in range(E):
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        w = random.randint(1, 1000)
        lines.append(f"{u} {v} {w}")

    Q = random.randint(10, 1000)
    lines.append(str(Q))
    for _ in range(Q):
        start = random.randint(0, V - 1)
        target = random.randint(0, V - 1)
        lines.append(f"{start} {target}")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle_checker"
    agent_path = "/home/user/checker"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(42)
    num_tests = 100

    for i in range(num_tests):
        test_input = generate_test_case()

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on test case {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on test case {i}.")

        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_output = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on test case {i}.")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent program crashed on test case {i}. Return code: {agent_proc.returncode}\nStderr: {agent_proc.stderr}")

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on test case {i}!\n"
                f"Input (first 100 chars): {test_input[:100]}...\n"
                f"Oracle output (first 100 chars): {oracle_output[:100]}...\n"
                f"Agent output (first 100 chars): {agent_output[:100]}..."
            )