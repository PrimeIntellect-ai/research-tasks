# test_final_state.py

import os
import json

def test_incident_report_exists_and_correct():
    report_path = "/home/user/incident_report.json"
    assert os.path.exists(report_path), f"Incident report is missing at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a file"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} does not contain valid JSON"

    assert "attacker_ip" in data, "Key 'attacker_ip' missing in incident report"
    assert data["attacker_ip"] == "10.55.201.88", f"Expected attacker_ip to be '10.55.201.88', got {data['attacker_ip']}"

    assert "vulnerable_header" in data, "Key 'vulnerable_header' missing in incident report"
    assert data["vulnerable_header"] == "X-Vip-Token", f"Expected vulnerable_header to be 'X-Vip-Token', got {data['vulnerable_header']}"

def test_waf_rules_exists_and_correct():
    waf_path = "/home/user/waf_rules.json"
    assert os.path.exists(waf_path), f"WAF rules file is missing at {waf_path}"
    assert os.path.isfile(waf_path), f"{waf_path} is not a file"

    with open(waf_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{waf_path} does not contain valid JSON"

    assert "blocked_ips" in data, "Key 'blocked_ips' missing in WAF rules"
    assert isinstance(data["blocked_ips"], list), "'blocked_ips' must be a list"
    assert "10.55.201.88" in data["blocked_ips"], "Attacker IP '10.55.201.88' is not in 'blocked_ips'"

    assert "blocked_headers" in data, "Key 'blocked_headers' missing in WAF rules"
    assert isinstance(data["blocked_headers"], list), "'blocked_headers' must be a list"
    assert "X-Vip-Token" in data["blocked_headers"], "Vulnerable header 'X-Vip-Token' is not in 'blocked_headers'"

def test_exploit_success_file_exists_and_correct():
    exploit_path = "/home/user/exploit_success.txt"
    assert os.path.exists(exploit_path), f"Exploit success file is missing at {exploit_path}. The exploit may not have succeeded."
    assert os.path.isfile(exploit_path), f"{exploit_path} is not a file"

    with open(exploit_path, 'r') as f:
        content = f.read().strip()

    assert content == "EXPLOITED", f"Expected exploit success file to contain exactly 'EXPLOITED', but got '{content}'"