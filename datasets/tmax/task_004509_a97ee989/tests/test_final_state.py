# test_final_state.py

import os
import random
import subprocess
import json
import urllib.request
import urllib.error
import tempfile
import pytest

def test_pipeline_end_to_end():
    """Test that the Nginx -> Flask -> Redis pipeline is working correctly."""
    url = "http://localhost:8080/data"
    test_value = 123.45
    data = json.dumps({"value": test_value}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.getcode() == 200, f"Expected HTTP 200 OK, got {response.getcode()}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the pipeline at {url}: {e}")

    # Check Redis
    try:
        result = subprocess.run(
            ["redis-cli", "LPOP", "sensor_data"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        popped_value = result.stdout.strip()
        # The API might store it as a string or float, but redis-cli returns a string
        assert popped_value == str(test_value), f"Expected {test_value} in Redis, got {popped_value}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("redis-cli not found, is Redis installed?")

def test_stable_stat_fuzz_equivalence():
    """Test that /home/user/stable_stat matches /app/oracle_stat bit-for-bit on random inputs."""
    agent_bin = "/home/user/stable_stat"
    oracle_bin = "/app/oracle_stat"

    assert os.path.isfile(agent_bin), f"Agent program {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent program {agent_bin} is not executable."
    assert os.path.isfile(oracle_bin), f"Oracle program {oracle_bin} does not exist."

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(100):
            num_lines = random.randint(10, 1000)
            input_file = os.path.join(tmpdir, f"input_{i}.txt")

            with open(input_file, "w") as f:
                for _ in range(num_lines):
                    val = random.uniform(-1e6, 1e6)
                    f.write(f"{val}\n")

            # Run oracle
            try:
                oracle_res = subprocess.run(
                    [oracle_bin, input_file],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
                oracle_output = oracle_res.stdout.strip()
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on input {i}: {e.stderr}")

            # Run agent
            try:
                agent_res = subprocess.run(
                    [agent_bin, input_file],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
                agent_output = agent_res.stdout.strip()
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Agent program failed on input {i}: {e.stderr}")

            assert agent_output == oracle_output, (
                f"Mismatch on iteration {i} (N={num_lines}).\n"
                f"Oracle output: {oracle_output}\n"
                f"Agent output:  {agent_output}"
            )