# test_final_state.py

import os
import sys
import json
import random
import string
import subprocess
import pytest

def test_vendored_package_fixed_and_installed():
    """Test that the vendored package bug is fixed and the package is installed."""
    connection_py_path = "/app/vendor/tunneled_smtp_client-0.9/tunneled_smtp_client/connection.py"

    assert os.path.isfile(connection_py_path), f"File {connection_py_path} is missing."

    with open(connection_py_path, 'r') as f:
        content = f.read()

    # The bug was "actual_ssh_port = 22"
    assert "actual_ssh_port = 22" not in content, "The bug 'actual_ssh_port = 22' is still present."
    # It should use self.ssh_port
    assert "self.ssh_port" in content, "The fix should use 'self.ssh_port'."

    # Check if package is installed in user environment
    result = subprocess.run([sys.executable, "-m", "pip", "show", "tunneled-smtp-client"], capture_output=True, text=True)
    assert result.returncode == 0, "Package tunneled_smtp_client is not installed."
    assert "Location:" in result.stdout

def generate_random_service_name():
    length = random.randint(3, 15)
    chars = string.ascii_lowercase + string.digits + "-"
    return "".join(random.choice(chars) for _ in range(length))

def generate_random_json_input():
    num_services = random.randint(1, 20)
    data = []
    errors = ["timeout", "connection refused", "503 bad gateway", "internal server error"]
    for _ in range(num_services):
        status = random.choice(["up", "down"])
        if status == "up":
            data.append({
                "service": generate_random_service_name(),
                "status": "up",
                "latency_ms": random.randint(1, 5000),
                "error": None
            })
        else:
            data.append({
                "service": generate_random_service_name(),
                "status": "down",
                "latency_ms": -1,
                "error": random.choice(errors)
            })
    return json.dumps(data)

def test_format_alert_fuzz_equivalence():
    """Test that format_alert.py matches oracle_format_alert on random inputs."""
    oracle_path = "/app/oracle_format_alert"
    agent_script = "/home/user/format_alert.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing."

    random.seed(42)

    for i in range(100):
        json_input = generate_random_json_input()

        oracle_proc = subprocess.run([oracle_path, json_input], capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {json_input}\nStderr: {oracle_proc.stderr}"

        agent_proc = subprocess.run([sys.executable, agent_script, json_input], capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on input: {json_input}\nStderr: {agent_proc.stderr}"

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input {i}:\n"
            f"Input: {json_input}\n"
            f"Expected (Oracle):\n{oracle_proc.stdout}\n"
            f"Got (Agent):\n{agent_proc.stdout}"
        )

def test_cron_job_setup():
    """Test that the cron job is correctly loaded into the crontab."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Is it installed?"

    expected_cron = "*/5 * * * * /home/user/run_monitor.sh"
    assert expected_cron in result.stdout, f"Crontab does not contain expected entry. Got:\n{result.stdout}"