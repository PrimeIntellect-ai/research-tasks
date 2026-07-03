# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_expression():
    ops = ['+', '-', '*', '/']
    expr = str(random.randint(1, 999))
    num_ops = random.randint(1, 4)
    for _ in range(num_ops):
        expr += f" {random.choice(ops)} {random.randint(1, 999)}"
    return expr

def test_evaluate_sh_exists_and_executable():
    script_path = "/home/user/evaluate.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/app/oracle_eval"
    agent_script = "/home/user/evaluate.sh"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} is missing from the environment."

    for _ in range(100):
        expr = generate_expression()

        oracle_cmd = [oracle_path, expr]
        agent_cmd = ["/bin/bash", agent_script, expr]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=5)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {expr}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=15)
            agent_out = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {expr}")

        assert agent_out == oracle_out, (
            f"Mismatch on input '{expr}'.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'\n"
            f"Agent stderr: '{agent_res.stderr.strip()}'"
        )