# test_final_state.py

import os
import json
import random
import string
import subprocess
import urllib.request
import time
import pytest

def test_services_running():
    """Verify that Nginx and the underlying services are properly configured and running."""
    # Test Nginx routing to user_service
    try:
        u_req = urllib.request.urlopen("http://127.0.0.1:8000/user/test_u")
        u_data = json.loads(u_req.read().decode('utf-8'))
        assert "embedding" in u_data, "User service response missing 'embedding'"
    except Exception as e:
        pytest.fail(f"Failed to reach user_service via Nginx on port 8000: {e}")

    # Test Nginx routing to item_service
    try:
        i_req = urllib.request.urlopen("http://127.0.0.1:8000/item/test_i")
        i_data = json.loads(i_req.read().decode('utf-8'))
        assert "category" in i_data and "price" in i_data, "Item service response missing expected fields"
    except Exception as e:
        pytest.fail(f"Failed to reach item_service via Nginx on port 8000: {e}")

def test_fuzz_equivalence():
    """Fuzz the agent's script against the oracle implementation."""
    agent_script = "/home/user/feature_extractor.py"
    oracle_script = "/tmp/oracle.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} does not exist."

    random.seed(42)

    def random_string(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    num_tests = 100
    for _ in range(num_tests):
        input_data = json.dumps({
            "user_id": random_string(),
            "item_id": random_string()
        })

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                ["python3", oracle_script, input_data],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {input_data}. Stderr: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_script, input_data],
                capture_output=True,
                text=True,
                check=True
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {input_data}. Stderr: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Output mismatch on input: {input_data}\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent): '{agent_out}'"
        )