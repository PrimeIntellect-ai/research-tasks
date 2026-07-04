# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_bin"
    agent_path = "/home/user/query_tool"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable: {agent_path}"

    random.seed(42)

    for _ in range(50):
        num_users = random.randint(1, 50)
        user_ids = random.sample(range(1, 1001), num_users)
        input_json = json.dumps(user_ids)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_json,
                text=True,
                capture_output=True,
                check=True,
                timeout=15
            )
            oracle_output = json.loads(oracle_proc.stdout)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {input_json}. Stderr: {e.stderr}")
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output invalid JSON on input {input_json}. Output: {oracle_proc.stdout}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {input_json}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_json,
                text=True,
                capture_output=True,
                check=True,
                timeout=15
            )
            agent_output = json.loads(agent_proc.stdout)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed on input {input_json}. Stderr: {e.stderr}")
        except json.JSONDecodeError:
            pytest.fail(f"Agent output invalid JSON on input {input_json}. Output: {agent_proc.stdout}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input {input_json}")

        assert agent_output == oracle_output, (
            f"Mismatch on input {input_json}.\n"
            f"Expected: {json.dumps(oracle_output, indent=2)}\n"
            f"Got: {json.dumps(agent_output, indent=2)}"
        )