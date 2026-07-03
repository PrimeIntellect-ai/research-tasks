# test_final_state.py

import os
import subprocess
import random
import pytest

def test_query_fixer_fuzz_equivalence():
    agent_script = "/home/user/query_fixer.py"
    oracle_binary = "/opt/oracle_query_fixer"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_binary), f"Oracle binary not found at {oracle_binary}"
    assert os.access(oracle_binary, os.X_OK), f"Oracle binary at {oracle_binary} is not executable"

    # Set a fixed seed for reproducibility
    random.seed(42)

    N = 100
    for i in range(N):
        page_number = random.randint(1, 20)
        page_size = random.randint(5, 50)

        # Run oracle
        oracle_cmd = [oracle_binary, str(page_number), str(page_size)]
        try:
            oracle_result = subprocess.run(
                oracle_cmd, capture_output=True, text=True, check=True, timeout=5
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input ({page_number}, {page_size}): {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input ({page_number}, {page_size})")

        # Run agent
        agent_cmd = ["python3", agent_script, str(page_number), str(page_size)]
        try:
            agent_result = subprocess.run(
                agent_cmd, capture_output=True, text=True, check=True, timeout=5
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input ({page_number}, {page_size}).\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input ({page_number}, {page_size})")

        # Compare outputs
        if agent_output != oracle_output:
            pytest.fail(
                f"Mismatch on input page_number={page_number}, page_size={page_size}.\n"
                f"Expected (Oracle):\n{oracle_output}\n\n"
                f"Got (Agent):\n{agent_output}"
            )