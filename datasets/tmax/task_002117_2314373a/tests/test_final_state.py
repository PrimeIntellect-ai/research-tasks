# test_final_state.py
import os
import urllib.request
import urllib.error
import json
import random
import subprocess
import pytest

def test_services_running_and_proxying():
    """Test that Nginx is running on 8080 and proxying to the FastAPI app."""
    url = "http://127.0.0.1:8080/compute"

    try:
        # First request to populate cache
        req1 = urllib.request.Request(url)
        with urllib.request.urlopen(req1, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))

        # Second request to hit cache
        req2 = urllib.request.Request(url)
        with urllib.request.urlopen(req2, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "success", "Expected status: success in JSON"

    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or error during request: {e}")
    except json.JSONDecodeError:
        pytest.fail("Response was not valid JSON")

def test_analyzer_fuzz_equivalence():
    """Test the analyzer.py script against the reference oracle using fuzz testing."""
    agent_script = "/home/user/analyzer.py"
    oracle_script = "/opt/verifier/reference_analyzer.py"

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script missing: {oracle_script}"

    # Check if executable
    assert os.access(agent_script, os.X_OK), f"{agent_script} is not executable"

    random.seed(42)
    num_tests = 500

    for i in range(num_tests):
        length = random.randint(10, 100)
        latencies = [str(random.randint(-50, 1500)) for _ in range(length)]
        input_str = ",".join(latencies)

        # Run oracle
        oracle_cmd = ["python3", oracle_script, input_str]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_str}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_cmd = ["python3", agent_script, input_str]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on input: {input_str}\nError: {agent_proc.stderr}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Output mismatch on input: {input_str}\n"
            f"Expected (Oracle): {oracle_output!r}\n"
            f"Got (Agent): {agent_output!r}"
        )