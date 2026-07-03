# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_token_gen_exists():
    path = "/home/user/token_gen.py"
    assert os.path.exists(path), f"Agent script not found at {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_fuzz_equivalence():
    oracle_path = "/app/auth_oracle"
    agent_script = "/home/user/token_gen.py"
    secret_salt = "3001383629"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    # Set up random seed for deterministic fuzzing
    random.seed(42)

    num_tests = 1000
    chars = string.ascii_letters + string.digits

    for i in range(num_tests):
        # Generate random user_id (length 4 to 16)
        user_id_len = random.randint(4, 16)
        user_id = "".join(random.choice(chars) for _ in range(user_id_len))

        # Generate random timestamp
        timestamp = str(random.randint(1600000000, 1800000000))

        # Run oracle
        oracle_cmd = [oracle_path, secret_salt, user_id, timestamp]
        try:
            oracle_res = subprocess.run(
                oracle_cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{user_id}' '{timestamp}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{user_id}' '{timestamp}'")

        # Run agent script
        agent_cmd = ["python3", agent_script, user_id, timestamp]
        try:
            agent_res = subprocess.run(
                agent_cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input '{user_id}' '{timestamp}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input '{user_id}' '{timestamp}'")

        assert agent_output == oracle_output, (
            f"Output mismatch on test {i+1}/{num_tests}!\n"
            f"Input user_id: {user_id}\n"
            f"Input timestamp: {timestamp}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )