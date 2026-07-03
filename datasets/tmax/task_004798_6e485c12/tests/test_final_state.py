# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_PATH = "/home/user/workspace/processor"

def generate_input(length):
    lines = []
    for _ in range(length):
        if random.random() < 0.10:
            lines.append("-1.0")
        else:
            val = random.uniform(10000.0, 10005.0)
            lines.append(f"{val:.6f}")
    return "\n".join(lines) + "\n"

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}. Did you compile it?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable."

def test_fuzz_equivalence_and_memory():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"

    random.seed(42)

    for i in range(100):
        length = random.randint(50, 500)
        window_size = random.randint(5, 50)
        input_data = generate_input(length)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, str(window_size)],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on run {i}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on run {i}.")

        # Run agent with valgrind
        try:
            agent_proc = subprocess.run(
                ["valgrind", "--error-exitcode=1", "--leak-check=full", AGENT_PATH, str(window_size)],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=10
            )
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed or leaked memory on run {i} (window_size={window_size}).\nReturn code: {e.returncode}\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on run {i} (window_size={window_size}).")

        if agent_out != oracle_out:
            pytest.fail(
                f"Output mismatch on run {i} (window_size={window_size}).\n"
                f"Input preview: {input_data[:200]}...\n"
                f"Expected (Oracle) output preview: {oracle_out[:300]}...\n"
                f"Actual (Agent) output preview: {agent_out[:300]}..."
            )