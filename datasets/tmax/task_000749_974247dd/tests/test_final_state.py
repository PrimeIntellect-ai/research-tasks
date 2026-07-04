# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import numpy as np
import pytest

def test_fuzz_equivalence():
    oracle_path = "/home/user/app/legacy/oracle_aggregator"
    agent_path = "/home/user/app/bin/fraud_aggregator"

    assert os.path.exists(oracle_path), f"Oracle binary is missing: {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary is missing: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable: {agent_path}"

    np.random.seed(42)

    for i in range(1000):
        num_ints = int(np.random.randint(100, 5001))
        # Generate random 32-bit signed integers
        input_data = np.random.randint(-2147483648, 2147483647, size=num_ints, dtype=np.int32).tobytes()

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on round {i}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        )

        if oracle_proc.stdout != agent_proc.stdout:
            oracle_out = oracle_proc.stdout.decode('ascii', errors='replace')
            agent_out = agent_proc.stdout.decode('ascii', errors='replace')
            pytest.fail(
                f"Output mismatch on round {i} with {num_ints} integers.\n"
                f"Oracle output:\n{oracle_out}\n"
                f"Agent output:\n{agent_out}"
            )

def test_api_endpoint():
    url = "http://localhost:8080/api/fraud_status"
    data = b"test payload"
    req = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"API request failed with HTTP error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"API request failed to connect: {e.reason}. Are the services running?")
    except Exception as e:
        pytest.fail(f"Unexpected error when hitting the API: {e}")