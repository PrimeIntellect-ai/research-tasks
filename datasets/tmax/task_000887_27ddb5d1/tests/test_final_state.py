# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_random_sequence(length):
    return ''.join(random.choice(['A', 'C', 'G', 'T']) for _ in range(length))

def test_evaluator_fuzz_equivalence():
    oracle_path = "/app/seq_evaluator"
    agent_code_path = "/home/user/evaluator.go"

    assert os.path.exists(oracle_path), f"Oracle binary missing: {oracle_path}"
    assert os.path.exists(agent_code_path), f"Agent Go code missing: {agent_code_path}"

    random.seed(42)
    num_tests = 500

    for _ in range(num_tests):
        seq_len = random.randint(10, 100)
        seq = generate_random_sequence(seq_len)

        # Run oracle
        try:
            oracle_result = subprocess.run(
                [oracle_path, seq],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {seq}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {seq}")

        # Run agent program
        try:
            agent_result = subprocess.run(
                ["go", "run", agent_code_path, seq],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {seq}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {seq}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input {seq}.\n"
            f"Oracle output: '{oracle_output}'\n"
            f"Agent output:  '{agent_output}'"
        )