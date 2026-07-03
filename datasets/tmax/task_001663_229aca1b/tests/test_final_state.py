# test_final_state.py

import os
import subprocess
import random
import pytest

def test_part1_explosion_frame():
    """Verify that the explosion frame index is correctly identified and written."""
    file_path = "/home/user/explosion_frame.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "142", f"Expected explosion frame to be '142', but got '{content}'."

def test_part2_stable_var_fuzzing():
    """Fuzz test the agent's stable_var.py against the oracle."""
    agent_script = "/home/user/stable_var.py"
    oracle_bin = "/app/oracle_stable_var"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} does not exist."

    random.seed(42)

    for i in range(500):
        # Generate random number of arguments between 0 and 500
        num_args = random.randint(0, 500)

        # Generate random floats, including positive, negative, large, and small values
        args = []
        for _ in range(num_args):
            val = random.uniform(-100000.0, 100000.0)
            args.append(f"{val:.6f}")

        # Run oracle
        oracle_cmd = [oracle_bin] + args
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on iteration {i} with args: {args[:10]}..."
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["python3", agent_script] + args
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on iteration {i} with args: {args[:10]}...\nStderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        # Compare
        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i}.\n"
            f"Input args (first 10): {args[:10]}...\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'"
        )