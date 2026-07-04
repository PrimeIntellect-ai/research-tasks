# test_final_state.py

import os
import json
import re
import subprocess
import pytest

def get_expected_app_data_size():
    total_size = 0
    for dirpath, _, filenames in os.walk("/home/user/app_data"):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def get_expected_default_gateway():
    with open("/home/user/mock_routes.txt", "r") as f:
        for line in f:
            if line.startswith("default via"):
                parts = line.split()
                if len(parts) >= 3:
                    return parts[2]
    return ""

def get_expected_timezone_match():
    with open("/home/user/config.json", "r") as f:
        config = json.load(f)
    expected_tz = config.get("timezone", "")

    with open("/home/user/mock_etc_timezone", "r") as f:
        actual_tz = f.read().strip()

    return expected_tz == actual_tz

def get_expected_rejected_ssh_hosts():
    rejected_hosts = []
    current_host = None

    with open("/home/user/mock_ssh_config", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Check for Host declaration
            host_match = re.match(r'(?i)^host\s+(.+)$', line)
            if host_match:
                current_host = host_match.group(1).strip()
                continue

            # Check for PubkeyAuthentication
            pubkey_match = re.match(r'(?i)^pubkeyauthentication\s+(no|yes)$', line)
            if pubkey_match and current_host:
                if pubkey_match.group(1).lower() == 'no':
                    rejected_hosts.append(current_host)

    return rejected_hosts

def test_system_audit_script_exists():
    script_path = "/home/user/system_audit.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_system_audit_script_runs():
    script_path = "/home/user/system_audit.py"
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed with error: {result.stderr}"

def test_audit_report_exists_and_valid_json():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"The report {report_path} was not generated."

    with open(report_path, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

def test_audit_report_contents():
    report_path = "/home/user/audit_report.json"
    with open(report_path, "r") as f:
        report = json.load(f)

    expected_size = get_expected_app_data_size()
    assert "app_data_size_bytes" in report, "Key 'app_data_size_bytes' missing in report."
    assert report["app_data_size_bytes"] == expected_size, f"Expected app_data_size_bytes to be {expected_size}, got {report['app_data_size_bytes']}."

    expected_gw = get_expected_default_gateway()
    assert "default_gateway" in report, "Key 'default_gateway' missing in report."
    assert report["default_gateway"] == expected_gw, f"Expected default_gateway to be '{expected_gw}', got '{report['default_gateway']}'."

    expected_tz_match = get_expected_timezone_match()
    assert "timezone_match" in report, "Key 'timezone_match' missing in report."
    assert report["timezone_match"] == expected_tz_match, f"Expected timezone_match to be {expected_tz_match}, got {report['timezone_match']}."

    expected_hosts = get_expected_rejected_ssh_hosts()
    assert "rejected_ssh_hosts" in report, "Key 'rejected_ssh_hosts' missing in report."
    assert isinstance(report["rejected_ssh_hosts"], list), "Key 'rejected_ssh_hosts' must be a list."
    assert sorted(report["rejected_ssh_hosts"]) == sorted(expected_hosts), f"Expected rejected_ssh_hosts to be {expected_hosts}, got {report['rejected_ssh_hosts']}."