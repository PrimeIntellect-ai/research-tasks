# test_final_state.py

import os
import subprocess
import random
import pytest

def test_evaluate_script_exists():
    assert os.path.isfile("/home/user/evaluate.py"), "The script /home/user/evaluate.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_eval"
    agent_script = "/home/user/evaluate.py"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"

    random.seed(42)
    inputs = [random.randint(-10000, 10000) for _ in range(1000)]

    for x in inputs:
        str_x = str(x)

        # Run oracle
        try:
            oracle_res = subprocess.run([oracle_path, str_x], capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {x}")

        assert oracle_res.returncode == 0, f"Oracle failed on input {x}. Stderr: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        try:
            agent_res = subprocess.run(["python3", agent_script, str_x], capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {x}")

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed on input {x}. Stderr: {agent_res.stderr}")

        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, f"Mismatch on input {x}. Expected: '{oracle_out}', Got: '{agent_out}'"