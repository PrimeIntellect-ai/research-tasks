# test_final_state.py

import os
import json
import pytest

def test_rotation_report_json():
    report_path = "/home/user/rotation_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_data = {
        "old_password": "LegacyPass9988!",
        "worker_bin_valid": True,
        "python_cwe": "CWE-798",
        "db_ip": "10.0.45.22"
    }

    for key, expected_val in expected_data.items():
        assert key in data, f"Key '{key}' missing from {report_path}."
        assert data[key] == expected_val, f"Expected '{key}' to be {expected_val}, but got {data[key]}."

def test_net_policy_json():
    policy_path = "/home/user/app_legacy/net_policy.json"
    assert os.path.isfile(policy_path), f"Network policy file {policy_path} does not exist."

    with open(policy_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {policy_path} is not valid JSON.")

    assert "allowed_ips" in data, f"'allowed_ips' missing from {policy_path}."
    assert "10.0.45.22" in data["allowed_ips"], f"IP '10.0.45.22' missing from 'allowed_ips' in {policy_path}."
    assert "action" in data, f"'action' missing from {policy_path}."
    assert data["action"] == "allow", f"Expected 'action' to be 'allow', but got {data['action']}."

def test_db_pass_txt():
    pass_path = "/home/user/secrets/db_pass.txt"
    assert os.path.isfile(pass_path), f"Password file {pass_path} does not exist."

    with open(pass_path, 'r') as f:
        content = f.read().strip()

    assert content == "SecureRotatedPass2024!", f"Expected password to be 'SecureRotatedPass2024!', but got '{content}'."

def test_service_py_modifications():
    service_path = "/home/user/app_legacy/service.py"
    assert os.path.isfile(service_path), f"Service script {service_path} does not exist."

    with open(service_path, 'r') as f:
        content = f.read()

    assert "LegacyPass9988!" not in content, f"Hardcoded password 'LegacyPass9988!' is still present in {service_path}."
    assert "/home/user/secrets/db_pass.txt" in content, f"Script {service_path} does not seem to read from '/home/user/secrets/db_pass.txt'."