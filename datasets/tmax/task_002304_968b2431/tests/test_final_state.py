# test_final_state.py

import os
import random
import subprocess
import pytest

def test_solution_exists():
    assert os.path.exists("/home/user/solution.py"), "/home/user/solution.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/telemetry_oracle"
    agent_cmd = ["python3", "/home/user/solution.py"]

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} missing."

    random.seed(42)

    for i in range(100):
        num_ints = random.randint(1, 50)
        ints = [str(random.randint(2, 100000)) for _ in range(num_ints)]
        input_str = " ".join(ints) + "\n"
        input_bytes = input_str.encode('utf-8')

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_bytes,
                capture_output=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {input_str}")

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_str}"
        oracle_output = oracle_proc.stdout

        # Run agent
        try:
            agent_proc = subprocess.run(
                agent_cmd,
                input=input_bytes,
                capture_output=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {input_str}")

        assert agent_proc.returncode == 0, f"Agent script failed on input: {input_str}\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Mismatch on fuzz test {i+1}.\n"
            f"Input: {input_str.strip()}\n"
            f"Oracle output (hex): {oracle_output.hex()}\n"
            f"Agent output (hex): {agent_output.hex()}"
        )