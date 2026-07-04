# test_final_state.py

import os
import hashlib
import ast
import pytest

def test_audit_report_exists_and_correct():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    endpoints_path = "/home/user/audit_target/endpoints.txt"
    assert os.path.isfile(endpoints_path), f"{endpoints_path} is missing, cannot compute hash."

    with open(endpoints_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"{report_path} should contain exactly two lines, found {len(lines)}."

    assert lines[0] == "COMPROMISED_FILE: endpoints.txt", f"First line of report is incorrect. Got: {lines[0]}"
    assert lines[1] == f"ACTUAL_HASH: {actual_hash}", f"Second line of report is incorrect. Got: {lines[1]} (Expected hash: {actual_hash})"

def test_generate_fw_py_exists_and_valid():
    script_path = "/home/user/generate_fw.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        source = f.read()

    try:
        ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"{script_path} contains invalid Python syntax: {e}")

def test_firewall_rules_sh_exists_and_correct():
    fw_path = "/home/user/firewall_rules.sh"
    assert os.path.isfile(fw_path), f"{fw_path} does not exist."

    with open(fw_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_rules = [
        "iptables -A INPUT -s 203.0.113.45 -j DROP",
        "iptables -A INPUT -s 198.51.100.99 -j DROP"
    ]

    # Check if the expected rules are present in the correct order
    actual_rules = [line for line in lines if line.startswith("iptables")]

    assert len(actual_rules) == 2, f"Expected exactly 2 iptables rules in {fw_path}, found {len(actual_rules)}."
    assert actual_rules[0] == expected_rules[0], f"First iptables rule is incorrect. Got: {actual_rules[0]}"
    assert actual_rules[1] == expected_rules[1], f"Second iptables rule is incorrect. Got: {actual_rules[1]}"