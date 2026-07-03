# test_final_state.py

import os
import json
import re
import pytest

def get_expected_state():
    headers_path = "/home/user/audit_data/headers.txt"
    log_path = "/home/user/audit_data/service.log"
    nmap_path = "/home/user/audit_data/scan.nmap"

    # 1. Extract leaked token
    leaked_token = None
    with open(headers_path, "r") as f:
        for line in f:
            if line.lower().startswith("x-old-cred-token:"):
                leaked_token = line.split(":", 1)[1].strip()
                break

    assert leaked_token is not None, "Could not find X-Old-Cred-Token in headers.txt"

    # 2. Extract compromised IPs
    compromised_ips = set()
    with open(log_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 10:
                continue
            ip = parts[0]
            # Standard combined log format: IP - - [date] "request" status bytes "-" "user-agent" "token"
            # We can use regex to parse it more reliably
            match = re.search(r'^(\S+).*" (\d{3}) \d+ ".*" ".*" "([^"]+)"\s*$', line)
            if match:
                log_ip, status, token = match.groups()
                if status == "200" and token == leaked_token:
                    compromised_ips.add(log_ip)

    # 3. Extract unauthorized ports
    unauthorized_ports = set()
    authorized = {22, 80, 443}
    with open(nmap_path, "r") as f:
        for line in f:
            match = re.match(r'^(\d+)/tcp\s+open\s+', line)
            if match:
                port = int(match.group(1))
                if port not in authorized:
                    unauthorized_ports.add(port)

    return {
        "leaked_token": leaked_token,
        "compromised_ips": sorted(list(compromised_ips)),
        "unauthorized_ports": sorted(list(unauthorized_ports))
    }

def test_audit_report_exists_and_valid():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Output file {report_path} is missing. The Rust program must generate this file."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_data = get_expected_state()

    assert "leaked_token" in report_data, "Key 'leaked_token' missing from JSON output."
    assert report_data["leaked_token"] == expected_data["leaked_token"], \
        f"Expected leaked_token '{expected_data['leaked_token']}', got '{report_data['leaked_token']}'"

    assert "compromised_ips" in report_data, "Key 'compromised_ips' missing from JSON output."
    assert isinstance(report_data["compromised_ips"], list), "'compromised_ips' must be a list."
    assert report_data["compromised_ips"] == expected_data["compromised_ips"], \
        f"Expected compromised_ips {expected_data['compromised_ips']}, got {report_data['compromised_ips']}"

    assert "unauthorized_ports" in report_data, "Key 'unauthorized_ports' missing from JSON output."
    assert isinstance(report_data["unauthorized_ports"], list), "'unauthorized_ports' must be a list."
    assert report_data["unauthorized_ports"] == expected_data["unauthorized_ports"], \
        f"Expected unauthorized_ports {expected_data['unauthorized_ports']}, got {report_data['unauthorized_ports']}"