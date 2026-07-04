# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/netdiag_obfuscated"
    agent_script = "/home/user/netdiag_replica.py"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)
    chars = string.ascii_letters + string.digits + ".:-_"

    for _ in range(1000):
        length = random.randint(1, 256)
        payload = "".join(random.choice(chars) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path, payload], capture_output=True, text=True)
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(["python3", agent_script, payload], capture_output=True, text=True)
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input '{payload}'\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )

def test_systemd_service_state():
    # Check if enabled
    enabled_proc = subprocess.run(
        ["systemctl", "--user", "is-enabled", "netdiag-replica.service"], 
        capture_output=True, text=True
    )
    assert enabled_proc.returncode == 0, f"Service is not enabled. systemctl output: {enabled_proc.stdout.strip()}"
    assert "enabled" in enabled_proc.stdout.strip(), "Service is not enabled"

    # Check if active
    active_proc = subprocess.run(
        ["systemctl", "--user", "is-active", "netdiag-replica.service"], 
        capture_output=True, text=True
    )
    assert active_proc.returncode == 0, f"Service is not active. systemctl output: {active_proc.stdout.strip()}"
    assert "active" in active_proc.stdout.strip(), "Service is not active"

def test_log_file_content():
    log_path = "/home/user/netdiag.log"
    assert os.path.exists(log_path), f"Log file does not exist at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    oracle_proc = subprocess.run(
        ["/app/netdiag_obfuscated", "DEFAULT_PAYLOAD"], 
        capture_output=True, text=True
    )
    expected_out = oracle_proc.stdout.strip()

    assert content == expected_out, f"Log content mismatch. Expected: {expected_out}, Got: {content}"