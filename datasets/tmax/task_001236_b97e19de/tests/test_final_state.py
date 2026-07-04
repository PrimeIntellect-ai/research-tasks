# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_random_graph(num_edges, max_node_id):
    edges = []
    for _ in range(num_edges):
        u = random.randint(1, max_node_id)
        v = random.randint(1, max_node_id)
        edges.append(f"{u} {v}")
    return "\n".join(edges) + "\n"

def test_projector_executable_exists():
    executable = "/home/user/projector"
    assert os.path.exists(executable), f"Executable {executable} does not exist."
    assert os.path.isfile(executable), f"{executable} is not a file."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_fuzz_equivalence():
    agent_executable = "/home/user/projector"
    oracle_executable = "/app/oracle_projector"

    assert os.path.exists(agent_executable), "Agent executable missing."
    assert os.path.exists(oracle_executable), "Oracle executable missing."

    random.seed(42)
    num_tests = 100

    for i in range(num_tests):
        num_edges = random.randint(50, 5000)
        input_data = generate_random_graph(num_edges, 1000)

        try:
            oracle_proc = subprocess.run(
                [oracle_executable],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on test case {i+1}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on test case {i+1}: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                [agent_executable],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_output = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on test case {i+1} with {num_edges} edges.")

        assert agent_proc.returncode == 0, f"Agent program failed with return code {agent_proc.returncode} on test case {i+1}. Stderr: {agent_proc.stderr}"

        if oracle_output != agent_output:
            # Truncate inputs and outputs for readable error message
            trunc_input = input_data[:200] + "..." if len(input_data) > 200 else input_data
            trunc_oracle = oracle_output[:200] + "..." if len(oracle_output) > 200 else oracle_output
            trunc_agent = agent_output[:200] + "..." if len(agent_output) > 200 else agent_output

            pytest.fail(
                f"Output mismatch on test case {i+1} with {num_edges} edges.\n"
                f"Input preview:\n{trunc_input}\n"
                f"Oracle output preview:\n{trunc_oracle}\n"
                f"Agent output preview:\n{trunc_agent}\n"
            )