# test_final_state.py

import os
import json
import pytest

def test_analyze_incident_script_exists():
    path = "/home/user/analyze_incident.py"
    assert os.path.isfile(path), f"Expected script {path} is missing."

def test_enforcement_report_exists():
    path = "/home/user/enforcement_report.json"
    assert os.path.isfile(path), f"Expected report file {path} is missing."

def test_enforcement_report_content():
    path = "/home/user/enforcement_report.json"
    assert os.path.isfile(path), f"Expected report file {path} is missing."

    with open(path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_ip = "172.16.0.42"
    expected_hash = "e382bbcdcf6071485dbce46fb2621189"
    expected_password = "devsecops2023"
    expected_cn = "EvilHacker"

    assert report.get("attacker_ip") == expected_ip, f"Expected attacker_ip to be '{expected_ip}', but got '{report.get('attacker_ip')}'."
    assert report.get("hardcoded_hash") == expected_hash, f"Expected hardcoded_hash to be '{expected_hash}', but got '{report.get('hardcoded_hash')}'."
    assert report.get("cracked_password") == expected_password, f"Expected cracked_password to be '{expected_password}', but got '{report.get('cracked_password')}'."
    assert report.get("cert_issuer_cn") == expected_cn, f"Expected cert_issuer_cn to be '{expected_cn}', but got '{report.get('cert_issuer_cn')}'."