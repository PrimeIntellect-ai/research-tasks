# test_final_state.py
import os
import json
import stat

def test_audit_trail_json():
    audit_file = "/home/user/audit_trail.json"
    assert os.path.isfile(audit_file), f"Audit trail file {audit_file} was not created."

    with open(audit_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{audit_file} does not contain valid JSON."

    assert "malicious_ips" in data, "Missing 'malicious_ips' key in audit trail."
    assert "quarantined_files" in data, "Missing 'quarantined_files' key in audit trail."

    expected_ips = ["10.0.0.55", "172.16.0.4", "192.168.1.11"]
    expected_files = ["file_beta.bin"]

    # Check malicious IPs (deduplicated and sorted)
    assert isinstance(data["malicious_ips"], list), "'malicious_ips' must be a list."
    assert sorted(data["malicious_ips"]) == expected_ips, f"Expected malicious_ips to be {expected_ips}, got {data['malicious_ips']}"

    # Check quarantined files (deduplicated and sorted)
    assert isinstance(data["quarantined_files"], list), "'quarantined_files' must be a list."
    assert sorted(data["quarantined_files"]) == expected_files, f"Expected quarantined_files to be {expected_files}, got {data['quarantined_files']}"

def test_quarantined_file_permissions():
    quarantined_file = "/home/user/uploads/file_beta.bin"
    assert os.path.isfile(quarantined_file), f"File {quarantined_file} does not exist."

    file_stat = os.stat(quarantined_file)
    file_mode = stat.S_IMODE(file_stat.st_mode)

    assert file_mode == 0o400, f"Expected permissions for {quarantined_file} to be 0400, got {oct(file_mode).replace('0o', '0')}"

def test_clean_file_permissions_unchanged():
    # Ensure clean files were not accidentally quarantined
    clean_files = [
        "/home/user/uploads/file_alpha.txt",
        "/home/user/uploads/file_gamma.jpg"
    ]
    for clean_file in clean_files:
        if os.path.isfile(clean_file):
            file_stat = os.stat(clean_file)
            file_mode = stat.S_IMODE(file_stat.st_mode)
            assert file_mode != 0o400, f"Clean file {clean_file} should not have 0400 permissions."