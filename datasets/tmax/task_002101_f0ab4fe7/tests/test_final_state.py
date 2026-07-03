# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/workspace/processor_fixed"

    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary at {oracle_path} is not executable"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    num_iterations = 100

    for i in range(num_iterations):
        num_ints = random.randint(1_000, 100_000)

        # Generate random integers
        ints = [str(random.randint(-10_000, 10_000)) for _ in range(num_ints)]
        input_data = " ".join(ints).encode('utf-8')

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True,
            timeout=10
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"
        oracle_output = oracle_proc.stdout.decode('utf-8').strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            capture_output=True,
            timeout=10
        )
        assert agent_proc.returncode == 0, f"Agent binary failed on iteration {i} with stderr: {agent_proc.stderr.decode('utf-8')}"
        agent_output = agent_proc.stdout.decode('utf-8').strip()

        # Compare outputs
        assert agent_output == oracle_output, (
            f"Mismatch on iteration {i}.\n"
            f"Input size: {num_ints} integers\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )