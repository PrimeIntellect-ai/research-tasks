# test_final_state.py
import os
import subprocess
import random

def test_user_cleaner_exists_and_executable():
    path = "/home/user/cleaner"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Expected {path} to be a file"
    assert os.access(path, os.X_OK), f"File {path} must be executable"

def test_no_subprocess_invocation():
    agent_path = "/home/user/cleaner"
    if os.path.exists(agent_path):
        with open(agent_path, "rb") as f:
            content = f.read()
        assert b"legacy_cleaner" not in content, "Agent program must not invoke the legacy_cleaner as a subprocess."

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_cleaner"
    agent_path = "/home/user/cleaner"

    assert os.path.exists(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.path.exists(agent_path), f"Agent missing: {agent_path}"

    # Use a fixed seed for reproducibility
    rng = random.Random(42)

    # Generate 100 random byte arrays
    for i in range(100):
        length = rng.randint(0, 10000)
        # Bytes drawn from the entire 0-255 range
        input_data = bytes(rng.randint(0, 255) for _ in range(length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                capture_output=True,
                timeout=5,
                check=False
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            assert False, f"Oracle timed out on iteration {i}"

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_data,
                capture_output=True,
                timeout=5,
                check=False
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            assert False, f"Agent timed out on iteration {i} (input length {length})"

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i} (input length {length}).\n"
            f"Input (first 50 bytes): {input_data[:50]!r}...\n"
            f"Oracle output (first 50 bytes): {oracle_out[:50]!r}...\n"
            f"Agent output (first 50 bytes): {agent_out[:50]!r}..."
        )