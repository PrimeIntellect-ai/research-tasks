# test_final_state.py

import os
import json
import re
import pytest
from collections import Counter

TRAFFIC_FILE = "/home/user/traffic.json"
AUDIT_SCRIPT = "/home/user/audit.py"
AUDIT_RESULTS = "/home/user/audit_results.json"
BLOCK_IP_SCRIPT = "/home/user/block_ip.sh"
SSHD_CONFIG = "/home/user/sshd_config"

def get_expected_audit_and_ip():
    assert os.path.isfile(TRAFFIC_FILE), f"Original traffic file {TRAFFIC_FILE} is missing."
    with open(TRAFFIC_FILE, 'r') as f:
        data = json.load(f)

    expected_results = []
    ip_counter = Counter()

    for req in data:
        headers = req.get("headers", {})
        cookie = headers.get("Cookie", "")
        if "admin_session" in cookie:
            ip_counter[req.get("source_ip")] += 1

            # Create a copy to redact
            redacted_req = {
                "source_ip": req.get("source_ip"),
                "headers": dict(headers)
            }
            if "Authorization" in redacted_req["headers"]:
                redacted_req["headers"]["Authorization"] = "[REDACTED]"

            expected_results.append(redacted_req)

    # Find IP with highest count
    if ip_counter:
        most_common_ip = ip_counter.most_common(1)[0][0]
    else:
        most_common_ip = None

    return expected_results, most_common_ip

def test_audit_results():
    assert os.path.isfile(AUDIT_RESULTS), f"Output file {AUDIT_RESULTS} does not exist."

    with open(AUDIT_RESULTS, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {AUDIT_RESULTS} is not valid JSON.")

    expected_results, _ = get_expected_audit_and_ip()

    assert actual_results == expected_results, f"The contents of {AUDIT_RESULTS} do not match the expected filtered and redacted output."

def test_audit_script_executable():
    assert os.path.isfile(AUDIT_SCRIPT), f"Audit script {AUDIT_SCRIPT} does not exist."
    assert os.access(AUDIT_SCRIPT, os.X_OK), f"Audit script {AUDIT_SCRIPT} is not executable."

def test_block_ip_script():
    assert os.path.isfile(BLOCK_IP_SCRIPT), f"Block IP script {BLOCK_IP_SCRIPT} does not exist."
    assert os.access(BLOCK_IP_SCRIPT, os.X_OK), f"Block IP script {BLOCK_IP_SCRIPT} is not executable."

    _, expected_ip = get_expected_audit_and_ip()
    assert expected_ip is not None, "Could not determine the target IP from the traffic log."

    expected_command = f"iptables -A INPUT -s {expected_ip} -j DROP"

    with open(BLOCK_IP_SCRIPT, 'r') as f:
        content = f.read().strip()

    # We can allow a shebang line, so we search for the exact command
    assert expected_command in content, f"The script {BLOCK_IP_SCRIPT} does not contain the expected iptables command: '{expected_command}'."

def test_sshd_config_hardened():
    assert os.path.isfile(SSHD_CONFIG), f"SSH config file {SSHD_CONFIG} does not exist."

    with open(SSHD_CONFIG, 'r') as f:
        lines = f.readlines()

    permit_root_login = False
    password_auth = False

    for line in lines:
        stripped = line.strip()
        if stripped == "PermitRootLogin no":
            permit_root_login = True
        elif stripped == "PasswordAuthentication no":
            password_auth = True

    assert permit_root_login, f"The setting 'PermitRootLogin no' was not found as an active configuration in {SSHD_CONFIG}."
    assert password_auth, f"The setting 'PasswordAuthentication no' was not found as an active configuration in {SSHD_CONFIG}."