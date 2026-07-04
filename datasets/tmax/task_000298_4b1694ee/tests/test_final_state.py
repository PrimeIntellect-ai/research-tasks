# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    """
    Fuzz test to ensure the agent's script matches the oracle's output exactly
    across a random sample of inputs.
    """
    agent_script = "/home/user/backup_extractor.py"
    oracle_script = "/app/oracle_extractor.py"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"

    # Fixed seed for reproducibility
    random.seed(42)

    num_iterations = 50
    for i in range(num_iterations):
        start_node = random.randint(1, 1000)
        max_depth = random.randint(1, 5)

        agent_cmd = ["python3", agent_script, "--start-node", str(start_node), "--max-depth", str(max_depth)]
        oracle_cmd = ["python3", oracle_script, "--start-node", str(start_node), "--max-depth", str(max_depth)]

        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)

        assert agent_proc.returncode == 0, (
            f"Agent script failed on input --start-node {start_node} --max-depth {max_depth}.\n"
            f"Stderr: {agent_proc.stderr}"
        )
        assert oracle_proc.returncode == 0, (
            f"Oracle script failed on input --start-node {start_node} --max-depth {max_depth}.\n"
            f"Stderr: {oracle_proc.stderr}"
        )

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input --start-node {start_node} --max-depth {max_depth}.\n"
            f"Agent output: {agent_out}\n"
            f"Oracle output: {oracle_out}"
        )