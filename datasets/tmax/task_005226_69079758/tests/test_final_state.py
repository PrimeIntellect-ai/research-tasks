# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    agent_file = "/home/user/backup_route.go"
    oracle_bin = "/app/oracle_bin"

    assert os.path.isfile(agent_file), f"Agent program not found at {agent_file}"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    nodes = ["NodeA", "NodeB", "NodeC", "NodeD", "NodeE", "MASTER"]

    random.seed(42)

    for i in range(50):
        node = random.choice(nodes)

        # Run oracle
        try:
            oracle_result = subprocess.run(
                [oracle_bin, node],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{node}': {e.stderr}")

        # Run agent
        try:
            agent_result = subprocess.run(
                ["go", "run", agent_file, node],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input '{node}'.\nStderr: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input '{node}'\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )