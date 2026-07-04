# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/secure_logger_oracle"
AGENT_PATH = "/home/user/secure_logger"
N_ITERATIONS = 1000

def generate_random_input(length):
    choice = random.random()
    if choice < 0.2:
        # Printable ASCII with some special chars
        chars = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n\t&<>\"'"
        return bytes(random.choice(chars) for _ in range(length))
    elif choice < 0.4:
        # Random bytes with a high chance of special chars
        res = bytearray()
        for _ in range(length):
            if random.random() < 0.1:
                res.append(random.choice(b"&<>\"'"))
            else:
                res.append(random.randint(0, 255))
        return bytes(res)
    else:
        # Pure random bytes
        return bytes(random.randint(0, 255) for _ in range(length))

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)  # Fixed seed for reproducibility

    for i in range(N_ITERATIONS):
        length = random.randint(0, 2048)
        test_input = generate_random_input(length)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=test_input,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i} with input length {length}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i} with input length {length}.")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=test_input,
                capture_output=True,
                timeout=2,
                check=True
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed on iteration {i} with input length {length}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on iteration {i} with input length {length}.")

        if oracle_output != agent_output:
            # Truncate output for display if it's too long
            disp_input = test_input[:100] + b"..." if len(test_input) > 100 else test_input
            disp_oracle = oracle_output[:100] + b"..." if len(oracle_output) > 100 else oracle_output
            disp_agent = agent_output[:100] + b"..." if len(agent_output) > 100 else agent_output

            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Input length: {length}\n"
                f"Input (truncated): {disp_input!r}\n"
                f"Oracle output (truncated): {disp_oracle!r}\n"
                f"Agent output (truncated): {disp_agent!r}"
            )