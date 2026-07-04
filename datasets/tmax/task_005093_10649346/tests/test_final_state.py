# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/solve.sh"
    oracle_bin = "/app/query_oracle"

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    random.seed(42)
    test_cases = [random.randint(1, 500) for _ in range(50)]

    for node_id in test_cases:
        node_id_str = str(node_id)

        # Run oracle
        oracle_cmd = [oracle_bin, node_id_str]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {node_id_str}. Stderr: {oracle_res.stderr}"

        # Run agent
        agent_cmd = ["/bin/bash", agent_script, node_id_str]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        # Compare
        assert agent_res.returncode == 0, f"Agent script failed on input {node_id_str}. Stderr: {agent_res.stderr}"

        oracle_output = oracle_res.stdout.strip()
        agent_output = agent_res.stdout.strip()

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on START_NODE_ID={node_id_str}.\n"
                f"Expected (Oracle):\n{oracle_output}\n"
                f"---\n"
                f"Got (Agent):\n{agent_output}"
            )