# test_final_state.py

import os
import random
import subprocess
import pytest

def test_transform_executable_exists():
    """Test that the agent's executable exists and is executable."""
    agent_path = "/home/user/transform"
    assert os.path.exists(agent_path), f"Agent's executable not found at {agent_path}"
    assert os.path.isfile(agent_path), f"Path {agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Agent's executable at {agent_path} is not executable"

def test_fuzz_equivalence():
    """Test that the agent's executable matches the oracle on random inputs."""
    oracle_path = "/app/oracle_transform"
    agent_path = "/home/user/transform"

    assert os.path.exists(oracle_path), f"Oracle executable not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent's executable not found at {agent_path}"

    random.seed(42)
    num_tests = 1000

    input_lines = []
    for _ in range(num_tests):
        a = random.randint(0, 10000)
        b = random.randint(0, 10000)
        c = random.randint(0, 10000)
        input_lines.append(f"{a} {b} {c}")

    input_data = "\n".join(input_lines) + "\n"

    try:
        oracle_process = subprocess.run(
            [oracle_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        oracle_output = oracle_process.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle process failed with error: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle process timed out.")

    try:
        agent_process = subprocess.run(
            [agent_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        agent_output = agent_process.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent process failed with return code {e.returncode}. Stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Agent process timed out. Ensure it reads from stdin until EOF.")

    assert len(agent_output) == len(oracle_output), \
        f"Output length mismatch. Expected {len(oracle_output)} lines, got {len(agent_output)} lines."

    for i, (expected, actual) in enumerate(zip(oracle_output, agent_output)):
        assert expected == actual, \
            f"Mismatch on line {i+1}. Input: '{input_lines[i]}'. Expected: '{expected}', Got: '{actual}'"