# test_final_state.py
import os
import json
import stat
import pytest

def test_security_report_json():
    report_path = "/home/user/security_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "suspicious_ips" in data, "JSON report missing 'suspicious_ips' key."
    assert "quarantined_files" in data, "JSON report missing 'quarantined_files' key."

    # Compute expected IPs from log
    log_path = "/home/user/logs/access.log"
    expected_ips = set()
    if os.path.isfile(log_path):
        with open(log_path, 'r') as f:
            for line in f:
                if "GET " in line:
                    parts = line.split()
                    if len(parts) > 6:
                        ip = parts[0]
                        req_path = parts[6]
                        if ".pem" in req_path or ".key" in req_path or "id_rsa" in req_path:
                            expected_ips.add(ip)

    expected_ips_sorted = sorted(list(expected_ips))
    assert data["suspicious_ips"] == expected_ips_sorted, f"Expected suspicious_ips {expected_ips_sorted}, got {data['suspicious_ips']}"

    expected_quarantined = sorted(["backup.txt", "dev_key.pem"])
    assert data["quarantined_files"] == expected_quarantined, f"Expected quarantined_files {expected_quarantined}, got {data['quarantined_files']}"

def test_quarantined_files_and_permissions():
    quarantine_dir = "/home/user/quarantine"
    expected_files = ["backup.txt", "dev_key.pem"]

    for filename in expected_files:
        filepath = os.path.join(quarantine_dir, filename)
        assert os.path.isfile(filepath), f"Expected quarantined file {filepath} is missing."

        # Check permissions (0600)
        st = os.stat(filepath)
        mode = stat.S_IMODE(st.st_mode)
        assert mode == 0o600, f"File {filepath} has incorrect permissions: {oct(mode)}, expected 0o600."

def test_original_files_removed():
    original_paths = [
        "/home/user/web_app/public/docs/backup.txt",
        "/home/user/web_app/public/dev_key.pem"
    ]

    for filepath in original_paths:
        assert not os.path.exists(filepath), f"Vulnerable file {filepath} was not removed from the web root."

def test_sshd_config_snippet():
    snippet_path = "/home/user/sshd_config.snippet"
    assert os.path.isfile(snippet_path), f"SSH config snippet {snippet_path} is missing."

    expected_lines = [
        "PermitRootLogin no",
        "PasswordAuthentication no",
        "X11Forwarding no",
        "MaxAuthTries 3"
    ]

    with open(snippet_path, 'r') as f:
        content = f.read().strip().splitlines()

    # Strip whitespace from each line for robust comparison
    actual_lines = [line.strip() for line in content if line.strip()]

    assert actual_lines == expected_lines, f"SSH config snippet content does not match exactly. Expected {expected_lines}, got {actual_lines}"