# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_log_processor"
AGENT_PATH = "/home/user/log_processor"
NUM_TESTS = 20  # Reduced from 1000 to 20 for reasonable test execution time
USER_IDS = ["U1", "U2", "ADMIN", "SVC1", "GUEST"]

def generate_fuzz_input(seed):
    rng = random.Random(seed)
    num_lines = rng.randint(100, 5000)
    lines = []
    for _ in range(num_lines):
        timestamp = rng.randint(1600000000, 1600010000)
        user_id = rng.choice(USER_IDS)
        cpu = rng.uniform(0.0, 1000.0)
        mem = rng.uniform(0.0, 1000.0)
        disk = rng.uniform(0.0, 1000.0)
        net = rng.uniform(0.0, 1000.0)
        lines.append(f"{timestamp} {user_id} {cpu:.4f} {mem:.4f} {disk:.4f} {net:.4f}")
    return "\n".join(lines) + "\n"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path is not a file: {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file is not executable: {AGENT_PATH}"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle is not executable: {ORACLE_PATH}"

    for i in range(NUM_TESTS):
        input_data = generate_fuzz_input(seed=42 + i)

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on test case {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on test case {i}.")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on test case {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on test case {i}.")

        if oracle_output != agent_output:
            # Truncate outputs for display if they are too long
            display_oracle = oracle_output if len(oracle_output) < 1000 else oracle_output[:1000] + "\n...[truncated]"
            display_agent = agent_output if len(agent_output) < 1000 else agent_output[:1000] + "\n...[truncated]"
            display_input = input_data if len(input_data) < 500 else input_data[:500] + "\n...[truncated]"

            error_msg = (
                f"Output mismatch on test case {i}!\n\n"
                f"Input (truncated):\n{display_input}\n\n"
                f"Oracle Output (truncated):\n{display_oracle}\n\n"
                f"Agent Output (truncated):\n{display_agent}\n"
            )
            pytest.fail(error_msg)