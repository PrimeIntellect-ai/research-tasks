# test_final_state.py
import os
import json
import stat
import re
import pytest

SERVICES_DIR = "/home/user/services"
LOG_FILE = "/home/user/logs/api_access.log"
FIREWALL_SCRIPT = "/home/user/firewall_block.sh"

def test_services_credentials_rotated():
    assert os.path.isdir(SERVICES_DIR), f"{SERVICES_DIR} directory is missing"

    alpha_path = os.path.join(SERVICES_DIR, "service_alpha.json")
    beta_path = os.path.join(SERVICES_DIR, "service_beta.json")
    gamma_path = os.path.join(SERVICES_DIR, "service_gamma.json")

    assert os.path.isfile(alpha_path), f"{alpha_path} is missing"
    with open(alpha_path, "r") as f:
        alpha_data = json.load(f)
    assert alpha_data.get("api_key") == "ROTATED_SEC_KEY_b7c2", "service_alpha.json api_key was not correctly rotated"

    assert os.path.isfile(gamma_path), f"{gamma_path} is missing"
    with open(gamma_path, "r") as f:
        gamma_data = json.load(f)
    assert gamma_data.get("api_key") == "ROTATED_SEC_KEY_b7c2", "service_gamma.json api_key was not correctly rotated"

    assert os.path.isfile(beta_path), f"{beta_path} is missing"
    with open(beta_path, "r") as f:
        beta_data = json.load(f)
    assert beta_data.get("api_key") == "VALID_KEY_xyz1", "service_beta.json api_key should not have been altered"

def test_firewall_script_exists_and_executable():
    assert os.path.isfile(FIREWALL_SCRIPT), f"{FIREWALL_SCRIPT} was not generated"
    st = os.stat(FIREWALL_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"{FIREWALL_SCRIPT} is not executable (missing chmod +x)"

def test_firewall_script_contents():
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} is missing"

    # Derive expected IPs from the log file
    malicious_ips = set()
    with open(LOG_FILE, "r") as f:
        for line in f:
            if "result: SUCCESS" in line and "KEY: EXPIRED_SYS_KEY_a8f9" in line:
                match = re.search(r"IP:\s*([\d\.]+)", line)
                if match:
                    ip = match.group(1)
                    if not ip.startswith("10.5."):
                        malicious_ips.add(ip)

    expected_lines = [f"iptables -A INPUT -s {ip} -j DROP" for ip in sorted(malicious_ips)]

    assert os.path.isfile(FIREWALL_SCRIPT), f"{FIREWALL_SCRIPT} is missing"
    with open(FIREWALL_SCRIPT, "r") as f:
        script_content = f.read().strip()

    actual_lines = [line.strip() for line in script_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Firewall script contents do not match expected.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )