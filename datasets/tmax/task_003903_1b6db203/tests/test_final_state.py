# test_final_state.py
import os
import subprocess
import random
import pytest

def test_agent_binary_exists():
    agent_path = "/home/user/build/smoother"
    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.path.isfile(agent_path), f"Path {agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_smoother"
    agent_path = "/home/user/build/smoother"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(42)

    num_tests = 100
    for i in range(num_tests):
        num_lines = random.randint(1, 200)
        input_lines = []
        for _ in range(num_lines):
            x = random.uniform(-5000.0, 5000.0)
            y = random.uniform(-5000.0, 5000.0)
            input_lines.append(f"{x:.6f} {y:.6f}")

        input_data = "\n".join(input_lines) + "\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent failed on iteration {i}:\n{agent_proc.stderr}"
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i} with {num_lines} lines.\n"
                f"Input preview: {input_data[:100]}...\n"
                f"Oracle output preview: {oracle_out[:100]}...\n"
                f"Agent output preview: {agent_out[:100]}..."
            )