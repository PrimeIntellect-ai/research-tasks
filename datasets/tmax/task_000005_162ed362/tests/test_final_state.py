# test_final_state.py

import os
import sys
import random
import string
import subprocess
import urllib.request
import pytest

def test_systemd_service_active():
    """Verify that the datashaper.service is running as a user service."""
    # Assuming the user is 'user' with UID 1000
    try:
        # Check via su to run as the user
        result = subprocess.run(
            ["su", "-", "user", "-c", "XDG_RUNTIME_DIR=/run/user/1000 systemctl --user is-active datashaper.service"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.stdout.strip() == "active", f"datashaper.service is not active. Output: {result.stdout.strip()}"
    except Exception as e:
        pytest.fail(f"Failed to check service status: {e}")

def test_port_forwarding_and_health_endpoint():
    """Verify that port 9090 is forwarded to 8080 and the service responds."""
    try:
        req = urllib.request.Request("http://localhost:9090/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            assert status == 200, f"Expected HTTP 200 from /health, got {status}"
    except Exception as e:
        pytest.fail(f"Failed to reach http://localhost:9090/health. Port forwarding or service may be broken: {e}")

def test_transform_fuzz_equivalence():
    """Fuzz test the agent's transform script against the oracle binary."""
    oracle_path = "/app/oracle_transform"
    agent_script = "/home/user/transform.py"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(5000):
        length = random.randint(1, 1000)
        test_input = "".join(random.choices(charset, k=length))

        # Run Oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_output = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle binary timed out.")

        # Run Agent Script
        try:
            agent_proc = subprocess.run(
                [sys.executable, agent_script],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_output = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Agent script timed out.")

        assert oracle_output == agent_output, (
            f"Mismatch on iteration {i+1}.\n"
            f"Input length: {length}\n"
            f"Oracle output: {oracle_output!r}\n"
            f"Agent output: {agent_output!r}"
        )