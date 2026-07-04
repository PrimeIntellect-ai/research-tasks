# test_final_state.py
import os
import random
import subprocess
import pytest

def test_fast_query_executable_exists():
    agent_executable = "/home/user/fast_query"
    assert os.path.exists(agent_executable), f"Agent executable {agent_executable} is missing."
    assert os.access(agent_executable, os.X_OK), f"Agent executable {agent_executable} is not executable."

def test_oracle_executable_exists():
    oracle_executable = "/app/oracle_fast_query"
    assert os.path.exists(oracle_executable), f"Oracle executable {oracle_executable} is missing."
    assert os.access(oracle_executable, os.X_OK), f"Oracle executable {oracle_executable} is not executable."

def test_fuzz_equivalence():
    agent_executable = "/home/user/fast_query"
    oracle_executable = "/app/oracle_fast_query"

    # Generate 50,000 random queries
    random.seed(42)
    N = 50000
    queries = []
    for _ in range(N):
        val = random.uniform(-2.0, 15.0)
        queries.append(f"{val:.4f}")

    input_data = "\n".join(queries) + "\n"

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_executable],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=30
        )
        oracle_output = oracle_proc.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to run: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle timed out.")

    # Run agent
    try:
        agent_proc = subprocess.run(
            [agent_executable],
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=30
        )
        agent_output = agent_proc.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent program failed to run: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out. Ensure it processes inputs efficiently.")

    # Compare outputs
    assert len(agent_output) == len(oracle_output), \
        f"Output length mismatch: expected {len(oracle_output)} lines, got {len(agent_output)} lines."

    for i, (expected, actual) in enumerate(zip(oracle_output, agent_output)):
        assert expected == actual, \
            f"Mismatch at query {i+1} (input: {queries[i]}). Expected: '{expected}', Got: '{actual}'"