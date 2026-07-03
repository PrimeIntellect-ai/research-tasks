# test_final_state.py

import os
import re
import pytest

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Flag file {flag_path} is missing."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{jwt_alg_none_c_binary_byp4ss}"
    assert content == expected_flag, f"Flag file content is incorrect. Expected {expected_flag}, but found: {content}"

def test_firewall_script_exists_and_correct():
    script_path = "/home/user/firewall.sh"
    assert os.path.isfile(script_path), f"Firewall script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read().strip()

    # Check for the correct iptables command
    # Matches variations like: iptables -A INPUT -p tcp --dport 13337 -j DROP
    pattern = r"iptables\s+-A\s+INPUT\s+-p\s+tcp\s+(?:--dport|--destination-port)\s+13337\s+-j\s+DROP"
    assert re.search(pattern, content), f"Firewall script does not contain the correct iptables command. Found: {content}"