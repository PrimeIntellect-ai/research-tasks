# test_final_state.py

import os
import hashlib
import re
from collections import Counter

def test_top_attacker_identified():
    auth_log_path = "/home/user/auth_log.txt"
    top_attacker_path = "/home/user/top_attacker.txt"

    assert os.path.isfile(auth_log_path), f"Input file {auth_log_path} is missing."
    assert os.path.isfile(top_attacker_path), f"Output file {top_attacker_path} is missing."

    # Derive the top attacker from the log
    failed_ips = []
    with open(auth_log_path, "r") as f:
        for line in f:
            if "Failed login" in line:
                match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                if match:
                    failed_ips.append(match.group(1))

    assert failed_ips, "No failed login attempts found in the log."

    ip_counts = Counter(failed_ips)
    expected_top_ip = ip_counts.most_common(1)[0][0]

    with open(top_attacker_path, "r") as f:
        actual_top_ip = f.read().strip()

    assert actual_top_ip == expected_top_ip, f"Expected top attacker IP '{expected_top_ip}', but got '{actual_top_ip}' in {top_attacker_path}."

def test_admin_password_cracked():
    auth_log_path = "/home/user/auth_log.txt"
    wordlist_path = "/home/user/wordlist.txt"
    admin_pass_path = "/home/user/admin_pass.txt"

    assert os.path.isfile(auth_log_path), f"Input file {auth_log_path} is missing."
    assert os.path.isfile(wordlist_path), f"Input file {wordlist_path} is missing."
    assert os.path.isfile(admin_pass_path), f"Output file {admin_pass_path} is missing."

    # Extract the admin hash
    admin_hash = None
    with open(auth_log_path, "r") as f:
        for line in f:
            if "Successful login" in line and "user admin" in line:
                match = re.search(r"with hash ([a-f0-9]{32})", line)
                if match:
                    admin_hash = match.group(1)
                    break

    assert admin_hash, "Could not find successful admin login hash in the log."

    # Crack the password using the wordlist
    expected_password = None
    with open(wordlist_path, "r") as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            if hashlib.md5(word.encode('utf-8')).hexdigest() == admin_hash:
                expected_password = word
                break

    assert expected_password, "Could not crack the admin password using the provided wordlist."

    with open(admin_pass_path, "r") as f:
        actual_password = f.read().strip()

    assert actual_password == expected_password, f"Expected cracked password '{expected_password}', but got '{actual_password}' in {admin_pass_path}."

def test_firewall_rule_generated():
    top_attacker_path = "/home/user/top_attacker.txt"
    fw_rule_path = "/home/user/fw_rule.txt"
    generate_fw_path = "/home/user/generate_fw.py"

    assert os.path.isfile(top_attacker_path), f"Output file {top_attacker_path} is missing."
    assert os.path.isfile(fw_rule_path), f"Output file {fw_rule_path} is missing."
    assert os.path.isfile(generate_fw_path), f"Script file {generate_fw_path} is missing."

    with open(top_attacker_path, "r") as f:
        top_ip = f.read().strip()

    expected_fw_rule = f"iptables -A INPUT -s {top_ip} -j DROP"

    with open(fw_rule_path, "r") as f:
        actual_fw_rule = f.read().strip()

    assert actual_fw_rule == expected_fw_rule, f"Expected firewall rule '{expected_fw_rule}', but got '{actual_fw_rule}' in {fw_rule_path}."