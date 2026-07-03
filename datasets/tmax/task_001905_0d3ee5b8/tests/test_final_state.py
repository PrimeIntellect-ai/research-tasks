# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    agent_path = "/home/user/metric_processor.sh"
    oracle_path = "/app/oracle_processor"

    # Check if the agent script exists and is executable
    assert os.path.isfile(agent_path), f"Agent script not found: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent script is not executable: {agent_path}"

    # Generate random inputs based on the distribution
    random.seed(42)
    inputs = []
    ports = [8080, 9090, 3000, 80, 443]
    for _ in range(1000):
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        port = random.choice(ports)
        duration = random.randint(0, 1500)
        inputs.append(f"{ip} {port} {duration}")

    input_str = "\n".join(inputs) + "\n"

    # Run the oracle
    oracle_proc = subprocess.run([oracle_path], input=input_str, text=True, capture_output=True)
    assert oracle_proc.returncode == 0, f"Oracle execution failed. Stderr: {oracle_proc.stderr}"

    # Run the agent script
    agent_proc = subprocess.run([agent_path], input=input_str, text=True, capture_output=True)

    # Compare outputs
    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    assert len(oracle_lines) == len(agent_lines), (
        f"Output line count mismatch. Expected {len(oracle_lines)} lines, got {len(agent_lines)} lines."
    )

    for in_line, o_line, a_line in zip(inputs, oracle_lines, agent_lines):
        assert o_line == a_line, (
            f"Mismatch on input: '{in_line}'\n"
            f"Expected (oracle): '{o_line}'\n"
            f"Got (agent)      : '{a_line}'"
        )