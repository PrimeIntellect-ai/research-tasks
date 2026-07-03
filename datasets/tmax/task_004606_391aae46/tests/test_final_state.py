# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_PATH = "/home/user/filter_aggregate"
NUM_TESTS = 200

def generate_csv_input(num_lines: int) -> str:
    lines = []
    for _ in range(num_lines):
        col1 = random.randint(-1000, 1000)
        col2 = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
        col3 = round(random.uniform(-100.0, 100.0), 2)
        lines.append(f"{col1},{col2},{col3:.2f}")
    return "\n".join(lines) + ("\n" if lines else "")

def test_agent_binary_exists():
    """Test that the agent's compiled binary exists and is executable."""
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    """Test that the agent's binary produces bit-exact identical output to the oracle."""
    random.seed(42)

    for i in range(NUM_TESTS):
        num_lines = random.randint(0, 1000)
        csv_input = generate_csv_input(num_lines)

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on test {i} with input:\n{csv_input}\nError: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on test {i} with input:\n{csv_input}\nError: {e.stderr}")

        if oracle_output != agent_output:
            pytest.fail(
                f"Output mismatch on test {i} (num_lines={num_lines}).\n"
                f"Input (first 10 lines):\n{chr(10).join(csv_input.splitlines()[:10])}\n...\n"
                f"Oracle Output (first 10 lines):\n{chr(10).join(oracle_output.splitlines()[:10])}\n"
                f"Agent Output (first 10 lines):\n{chr(10).join(agent_output.splitlines()[:10])}\n"
            )