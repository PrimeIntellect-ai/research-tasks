# test_final_state.py
import os
import json
import re

def test_ssh_config_fixed():
    config_path = "/home/user/.ssh/config"
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        content = f.read()

    # Check that PubkeyAuthentication no is removed or changed to yes
    assert not re.search(r'(?i)^\s*PubkeyAuthentication\s+no', content, re.MULTILINE), "SSH config still disables PubkeyAuthentication."

    # Check that IdentityFile is set
    assert re.search(r'(?i)^\s*IdentityFile\s+/home/user/\.ssh/migration_key', content, re.MULTILINE), "SSH config does not specify IdentityFile /home/user/.ssh/migration_key."

def test_python_script_fixed():
    script_path = "/home/user/validate_deployment.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()

    assert "try" in content and "except" in content, "Python script does not contain a try-except block for error handling."

def test_report_json_generated():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"{report_path} was not generated."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON."

    expected_data = {
        "web": "OK",
        "email": "MISSING_CERT"
    }

    assert report_data == expected_data, f"Report data {report_data} does not match expected {expected_data}."