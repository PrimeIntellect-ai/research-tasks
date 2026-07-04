# test_final_state.py

import os
import re
import pytest

def get_expected_values():
    server_script_path = "/home/user/server/server.py"
    default_payload = "IP:10.50.200.15;PORT:6666;FLAG:PT_SECURE_8484_ZZ"
    payload = default_payload

    if os.path.exists(server_script_path):
        with open(server_script_path, 'r') as f:
            content = f.read()
        m = re.search(r'payload_str\s*=\s*["\'](.*?)["\']', content)
        if m:
            payload = m.group(1)

    ip_match = re.search(r'IP:([^;]+)', payload)
    port_match = re.search(r'PORT:([^;]+)', payload)
    flag_match = re.search(r'FLAG:([^;]+)', payload)

    assert ip_match and port_match and flag_match, "Could not parse payload from server script."

    return ip_match.group(1), port_match.group(1), flag_match.group(1)

def test_flag_file_contents():
    _, _, expected_flag = get_expected_values()
    flag_path = "/home/user/flag.txt"

    assert os.path.isfile(flag_path), f"The file {flag_path} does not exist."

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_flag, f"The content of {flag_path} is incorrect. Expected '{expected_flag}', got '{content}'."

def test_block_vuln_script():
    expected_ip, expected_port, _ = get_expected_values()
    script_path = "/home/user/block_vuln.sh"

    assert os.path.isfile(script_path), f"The file {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # Pattern strictly matches the required iptables command as described in the truth
    pattern = rf"iptables\s+-A\s+OUTPUT\s+-p\s+tcp\s+-d\s+{re.escape(expected_ip)}\s+--dport\s+{re.escape(expected_port)}\s+-j\s+DROP"

    assert re.search(pattern, content), (
        f"The script {script_path} does not contain the correct iptables command. "
        f"Expected it to block outbound tcp traffic to IP {expected_ip} on port {expected_port}."
    )