# test_final_state.py

import os
import subprocess
import random
import urllib.request
import json
import pytest

def test_api_running_and_correct():
    """Verify that the Flask API is running, successfully connected to Redis, and returning the correct parameters."""
    url = "http://localhost:5000/api/params"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            assert "alpha" in data, "API response missing 'alpha' key"
            assert "N" in data, "API response missing 'N' key"
            assert data["alpha"] == 0.25, f"API returned wrong alpha: {data['alpha']}"
            assert data["N"] == 50, f"API returned wrong N: {data['N']}"
    except Exception as e:
        pytest.fail(f"Failed to connect to Flask API at {url} or received invalid response. Ensure the API is running and connected to Redis. Error: {e}")

def test_fuzz_equivalence():
    """Fuzz the agent's sequence processor against the oracle binary using 100 random DNA sequences."""
    agent_script = "/home/user/process_seq.py"
    oracle_bin = "/app/oracle_process"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']

    for _ in range(100):
        length = random.randint(20, 500)
        seq = "".join(random.choices(bases, k=length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_bin, seq],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle binary failed unexpectedly on input {seq}.\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input {seq}.")

        # Run agent script
        try:
            agent_res = subprocess.run(
                ["python3", agent_script, seq],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {seq}.\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {seq}.")

        assert agent_out == oracle_out, (
            f"Output mismatch on input sequence of length {length}:\n"
            f"Input: {seq}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )