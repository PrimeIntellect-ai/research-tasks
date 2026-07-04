# test_final_state.py
import json
import os
import base64
import stat
import pytest

def get_expected_key():
    """Dynamically extract and decode the expected key from the proc_dumps if possible."""
    try:
        with open('/home/user/proc_dumps/202_cmdline', 'rb') as f:
            parts = f.read().split(b'\x00')
            if b'--auth-token' in parts:
                idx = parts.index(b'--auth-token')
                b64_key = parts[idx+1]
                return base64.b64decode(b64_key).decode('utf-8')
    except Exception:
        pass
    return "-----BEGIN OPENSSH PRIVATE KEY-----\nbababooey12345\n-----END OPENSSH PRIVATE KEY-----"

def test_audit_report_json():
    report_path = '/home/user/audit_report.json'
    assert os.path.exists(report_path), f"Audit report not found at {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert isinstance(data, list), "Audit report JSON must be a list of dictionaries."
    assert len(data) == 1, f"Expected exactly 1 entry in the audit report, found {len(data)}."

    entry = data[0]
    assert "pid" in entry, "Missing 'pid' key in report entry."
    assert "uid" in entry, "Missing 'uid' key in report entry."
    assert "leaked_key" in entry, "Missing 'leaked_key' key in report entry."

    assert entry["pid"] == 202, f"Expected pid 202, got {entry['pid']}"
    assert entry["uid"] == 0, f"Expected uid 0, got {entry['uid']}"

    expected_key = get_expected_key()
    assert entry["leaked_key"] == expected_key, "The leaked_key in the report does not match the decoded payload."

def test_leaked_ssh_key_file():
    key_path = '/home/user/.ssh/leaked_id_rsa'
    assert os.path.exists(key_path), f"Leaked SSH key file not found at {key_path}"

    file_stat = os.stat(key_path)
    mode = stat.S_IMODE(file_stat.st_mode)
    assert oct(mode) == '0o600', f"Permissions for {key_path} should be 600, got {oct(mode)}"

    with open(key_path, 'r') as f:
        content = f.read()

    expected_key = get_expected_key()
    assert content == expected_key, "The content of the leaked_id_rsa file is incorrect."

def test_ssh_config_file():
    config_path = '/home/user/.ssh/config'
    assert os.path.exists(config_path), f"SSH config file not found at {config_path}"

    with open(config_path, 'r') as f:
        content = f.read()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    host_found = any(line.startswith('Host ') and 'audit-target' in line for line in lines)
    assert host_found, "Host entry 'audit-target' not found in SSH config."

    identity_found = any(line.lower().startswith('identityfile ') and '/home/user/.ssh/leaked_id_rsa' in line for line in lines)
    assert identity_found, "IdentityFile directive with correct path not found in SSH config."

    identities_only_found = any(line.lower().startswith('identitiesonly ') and 'yes' in line.lower() for line in lines)
    assert identities_only_found, "IdentitiesOnly yes directive not found in SSH config."

    password_auth_found = any(line.lower().startswith('passwordauthentication ') and 'no' in line.lower() for line in lines)
    assert password_auth_found, "PasswordAuthentication no directive not found in SSH config."