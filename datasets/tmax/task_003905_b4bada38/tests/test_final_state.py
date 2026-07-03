# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import random
import pytest

def test_api_health_check():
    """Check if the API can connect to the database."""
    url = "http://localhost:8080/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url} or API health check failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when checking {url}: {e}")

def test_compute_stats_fuzz_equivalence():
    """Fuzz equivalence test for compute_stats.sh against oracle_stats."""
    agent_script = "/home/user/compute_stats.sh"
    oracle_script = "/app/oracle_stats"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)

    for i in range(500):
        # Generate random CSV
        num_lines = random.randint(0, 50)
        csv_lines = ["id,val1,val2"]
        for _ in range(num_lines):
            id_val = random.randint(1, 100)
            val1 = random.uniform(-1000.0, 1000.0)
            val2 = random.uniform(-1000.0, 1000.0)
            csv_lines.append(f"{id_val},{val1:.5f},{val2:.5f}")

        csv_data = "\n".join(csv_lines) + "\n"
        csv_bytes = csv_data.encode("utf-8")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_script],
                input=csv_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on fuzz iteration {i}.")

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_script],
                input=csv_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle script timed out on fuzz iteration {i}.")

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz iteration {i}.\n"
            f"Input:\n{csv_data}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}\n"
            f"Agent stderr: {agent_proc.stderr!r}"
        )