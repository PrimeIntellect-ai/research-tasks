# test_final_state.py

import os
import subprocess
import tempfile
import random
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_SCRIPT = "/home/user/process_signal.py"
N_TESTS = 200

def generate_random_input(filepath, num_lines):
    with open(filepath, 'w') as f:
        for _ in range(num_lines):
            val = random.uniform(-1000.0, 1000.0)
            f.write(f"{val:.6f}\n")

def test_fuzz_equivalence():
    """Fuzz the agent's script against the oracle processor."""
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle processor not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle processor is not executable"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "input.txt")

        for i in range(N_TESTS):
            num_lines = random.randint(1000, 15000)
            generate_random_input(input_file, num_lines)

            # Run oracle
            oracle_cmd = [ORACLE_PATH, input_file]
            try:
                oracle_result = subprocess.run(
                    oracle_cmd, capture_output=True, text=True, check=True, timeout=5
                )
                oracle_output = oracle_result.stdout.strip()
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on test {i+1}: {e.stderr}")
            except subprocess.TimeoutExpired:
                pytest.fail(f"Oracle timed out on test {i+1}")

            # Run agent
            agent_cmd = ["python3", AGENT_SCRIPT, input_file]
            try:
                agent_result = subprocess.run(
                    agent_cmd, capture_output=True, text=True, check=True, timeout=5
                )
                agent_output = agent_result.stdout.strip()
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Agent script failed on test {i+1}: {e.stderr}")
            except subprocess.TimeoutExpired:
                pytest.fail(f"Agent script timed out on test {i+1}")

            assert agent_output == oracle_output, (
                f"Mismatch on test {i+1} with {num_lines} lines.\n"
                f"Oracle output: '{oracle_output}'\n"
                f"Agent output: '{agent_output}'"
            )