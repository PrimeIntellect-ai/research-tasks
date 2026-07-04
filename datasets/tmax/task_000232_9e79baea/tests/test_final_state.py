# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_redacted_session_file():
    """Verify the redacted session ID was saved correctly."""
    filepath = "/home/user/redacted_session.txt"
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read()

    expected_content = "root********\n"
    assert content == expected_content, f"Content of {filepath} is incorrect. Expected {repr(expected_content)}, got {repr(content)}"

def test_hash_generator_exists_and_executable():
    """Verify the hash generator script exists and is executable."""
    generator_path = "/home/user/hash_generator"
    assert os.path.exists(generator_path), f"Hash generator {generator_path} does not exist."
    assert os.path.isfile(generator_path), f"{generator_path} is not a regular file."
    assert os.access(generator_path, os.X_OK), f"{generator_path} is not executable."

def test_fuzz_equivalence_hash_generator():
    """Fuzz test the student's hash generator against the oracle."""
    oracle_path = "/app/auth_oracle"
    agent_path = "/home/user/hash_generator"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} missing."
    assert os.path.exists(agent_path), f"Agent executable {agent_path} missing."

    # Use a fixed seed for reproducible fuzzing
    random.seed(42)
    charset = string.ascii_letters + string.digits + "_-"

    for i in range(1000):
        length = random.randint(8, 64)
        test_input = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {repr(test_input)}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {repr(test_input)}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path, test_input],
                capture_output=True,
                text=True,
                timeout=2,
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input {repr(test_input)}")

        assert agent_proc.returncode == 0, f"Agent failed on input {repr(test_input)} with return code {agent_proc.returncode}. Stderr: {agent_proc.stderr}"

        assert agent_output == oracle_output, (
            f"Output mismatch on iteration {i+1}.\n"
            f"Input: {repr(test_input)}\n"
            f"Oracle output: {repr(oracle_output)}\n"
            f"Agent output:  {repr(agent_output)}"
        )