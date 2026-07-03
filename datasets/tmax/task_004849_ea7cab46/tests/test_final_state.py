# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_filter"
AGENT_PATH = "/home/user/signal_filter/target/release/signal_filter"
NUM_TESTS = 100
NUM_FLOATS = 10000

def test_agent_binary_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}. Did the build succeed?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable."

def test_oracle_binary_exists_and_executable():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable."

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(NUM_TESTS):
        # Generate random floats
        floats = [random.uniform(-100.0, 100.0) for _ in range(NUM_FLOATS)]
        input_str = " ".join(f"{x:.6f}" for x in floats)
        input_bytes = input_str.encode('utf-8')

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            capture_output=True,
            timeout=10
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on test {i} with stderr: {oracle_proc.stderr.decode()}"
        oracle_output = oracle_proc.stdout.decode('utf-8')

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            capture_output=True,
            timeout=10
        )
        assert agent_proc.returncode == 0, f"Agent failed on test {i} with stderr: {agent_proc.stderr.decode()}"
        agent_output = agent_proc.stdout.decode('utf-8')

        # Compare outputs
        if oracle_output != agent_output:
            # Truncate output for error message if it's too long
            trunc_oracle = oracle_output[:200] + ("..." if len(oracle_output) > 200 else "")
            trunc_agent = agent_output[:200] + ("..." if len(agent_output) > 200 else "")
            trunc_input = input_str[:200] + ("..." if len(input_str) > 200 else "")

            pytest.fail(
                f"Mismatch on test {i}.\n"
                f"Input (truncated): {trunc_input}\n"
                f"Oracle output (truncated): {trunc_oracle}\n"
                f"Agent output (truncated): {trunc_agent}\n"
            )