# test_final_state.py

import os
import random
import subprocess
import pytest

def test_analyzer_executable_exists():
    """Check if the agent's executable exists and is executable."""
    agent_executable = "/home/user/analyzer"
    assert os.path.isfile(agent_executable), f"Agent executable not found at {agent_executable}"
    assert os.access(agent_executable, os.X_OK), f"Agent executable at {agent_executable} is not executable"

def test_oracle_executable_exists():
    """Check if the oracle executable exists and is executable."""
    oracle_executable = "/opt/oracle/analyzer"
    assert os.path.isfile(oracle_executable), f"Oracle executable not found at {oracle_executable}"
    assert os.access(oracle_executable, os.X_OK), f"Oracle executable at {oracle_executable} is not executable"

def test_fuzz_equivalence():
    """Fuzz the agent's analyzer against the reference oracle."""
    agent_executable = "/home/user/analyzer"
    oracle_executable = "/opt/oracle/analyzer"

    random.seed(42)

    for i in range(100):
        # Generate input length between 100 and 10000
        num_floats = random.randint(100, 10000)
        # Generate floats uniformly from [-0.5, 2.5]
        floats = [random.uniform(-0.5, 2.5) for _ in range(num_floats)]
        input_data = ",".join(f"{f:.6f}" for f in floats).encode('utf-8')

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_executable],
            input=input_data,
            capture_output=True,
            timeout=5
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i} with error: {oracle_proc.stderr.decode()}"
        oracle_output = oracle_proc.stdout.decode('utf-8').strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_executable],
            input=input_data,
            capture_output=True,
            timeout=5
        )
        assert agent_proc.returncode == 0, f"Agent failed on input {i} with error: {agent_proc.stderr.decode()}"
        agent_output = agent_proc.stdout.decode('utf-8').strip()

        # Compare outputs
        assert agent_output == oracle_output, (
            f"Mismatch on fuzz input {i} (length {num_floats}).\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}\n"
            f"Input sample (first 100 chars): {input_data[:100].decode('utf-8')}..."
        )