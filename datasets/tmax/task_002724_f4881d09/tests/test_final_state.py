# test_final_state.py
import os
import subprocess
import random
import pytest

AGENT_SCRIPT = "/home/user/optimized_flow.py"
ORACLE_BINARY = "/app/legacy_flow_calc"

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} is missing."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary {ORACLE_BINARY} is missing."
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} is missing."

    random.seed(42)
    test_cases = [random.randint(1, 10000) for _ in range(100)]

    for node_id in test_cases:
        node_id_str = str(node_id)

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [ORACLE_BINARY, node_id_str],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on node ID {node_id}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on node ID {node_id}: {e.stderr}")

        # Run agent
        try:
            agent_res = subprocess.run(
                ["python3", AGENT_SCRIPT, node_id_str],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on node ID {node_id}. It must be optimized.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on node ID {node_id}: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on node ID {node_id}.\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )