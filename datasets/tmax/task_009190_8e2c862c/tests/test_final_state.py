# test_final_state.py

import os
import subprocess
import re

def compute_hash(data: str, key: str) -> str:
    """Recompute the XOR hash as done in the C++ service."""
    out = ""
    for i in range(len(data)):
        c = ord(data[i]) ^ ord(key[i % len(key)])
        out += f"{c:02x}"
    return out

def test_auth_server_cpp_updated():
    filepath = "/home/user/auth_server.cpp"
    assert os.path.isfile(filepath), f"Missing required file: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    assert "NEW_SECURE_KEY_2024" in content, "The file auth_server.cpp does not contain the new secure key."
    assert "LEGACY_KEY_884" not in content, "The file auth_server.cpp still contains the legacy key."

def test_auth_server_compiled():
    filepath = "/home/user/auth_server"
    assert os.path.isfile(filepath), f"Compiled binary missing: {filepath}"
    assert os.access(filepath, os.X_OK), f"File is not executable: {filepath}"

def test_admin_payload_format_and_content():
    filepath = "/home/user/admin_payload.http"
    assert os.path.isfile(filepath), f"Missing required file: {filepath}"

    with open(filepath, "r") as f:
        content = f.read()

    # Check for Cookie header
    match = re.search(r"Cookie:\s*session=([^:\r\n]+):([a-fA-F0-9]+)", content)
    assert match is not None, "admin_payload.http does not contain a correctly formatted Cookie header."

    data, hash_val = match.groups()
    assert data == "role=admin", f"Expected data to be 'role=admin', got '{data}'"

    expected_hash = compute_hash("role=admin", "NEW_SECURE_KEY_2024")
    assert hash_val.lower() == expected_hash.lower(), f"Expected hash {expected_hash}, got {hash_val}"

def test_auth_server_execution_with_payload():
    binary = "/home/user/auth_server"
    payload = "/home/user/admin_payload.http"

    assert os.path.isfile(binary), f"Missing binary: {binary}"
    assert os.path.isfile(payload), f"Missing payload: {payload}"

    with open(payload, "r") as f:
        payload_data = f.read()

    result = subprocess.run([binary], input=payload_data, text=True, capture_output=True)

    assert "Access Granted: Admin" in result.stdout, (
        f"Expected 'Access Granted: Admin' in output, got: {result.stdout.strip()}"
    )

def test_firewall_rules_generated_correctly():
    filepath = "/home/user/firewall_rules.sh"
    assert os.path.isfile(filepath), f"Missing required file: {filepath}"

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    expected_ips = ["172.16.0.4", "198.51.100.2", "203.0.113.8"]
    expected_lines = [f"iptables -A INPUT -s {ip} -j DROP" for ip in expected_ips]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} iptables rules, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Rule {i+1} mismatch. Expected '{expected}', got '{actual}'"