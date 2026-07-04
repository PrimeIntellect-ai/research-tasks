# test_final_state.py
import json
import os

def test_ssh_keys_generated():
    private_key = '/home/user/.ssh/log_backup_key'
    public_key = '/home/user/.ssh/log_backup_key.pub'

    assert os.path.exists(private_key), f"Private key missing at {private_key}"
    assert os.path.exists(public_key), f"Public key missing at {public_key}"

    with open(private_key, 'r') as f:
        content = f.read()
        assert 'OPENSSH PRIVATE KEY' in content, "The private key is not a valid OpenSSH format (expected Ed25519)."

def test_ssh_config_hardened():
    config_path = '/home/user/.ssh/config'
    assert os.path.exists(config_path), f"SSH config missing at {config_path}"

    with open(config_path, 'r') as f:
        config_content = f.read().lower()

    assert 'host backup.local' in config_content, "Host backup.local is not configured in SSH config."
    assert 'passwordauthentication no' in config_content, "PasswordAuthentication is not set to 'no'."
    assert 'identityfile /home/user/.ssh/log_backup_key' in config_content, "IdentityFile is not properly set to the generated key."

def test_redacted_logs_content():
    redacted_path = '/home/user/redacted_logs.jsonl'
    assert os.path.exists(redacted_path), f"Redacted logs file missing at {redacted_path}"

    expected_logs = [
        {"timestamp": "2023-10-01T12:00:00Z", "method": "GET", "url": "/profile", "headers": {"Host": "example.com", "Authorization": "[REDACTED]", "Cookie": "theme=dark; session_id=[REDACTED]; lang=en", "User-Agent": "curl/7.68.0"}},
        {"timestamp": "2023-10-01T12:00:05Z", "method": "POST", "url": "/login", "headers": {"Host": "example.com", "Content-Type": "application/json"}},
        {"timestamp": "2023-10-01T12:00:10Z", "method": "GET", "url": "/dashboard", "headers": {"Host": "example.com", "Cookie": "session_id=[REDACTED]; active=true", "Authorization": "[REDACTED]"}}
    ]

    actual_logs = []
    with open(redacted_path, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    actual_logs.append(json.loads(line))
                except json.JSONDecodeError:
                    assert False, f"Line in {redacted_path} is not valid JSON."

    assert len(actual_logs) == len(expected_logs), f"Expected {len(expected_logs)} lines in redacted logs, found {len(actual_logs)}."

    for i, (actual, expected) in enumerate(zip(actual_logs, expected_logs)):
        assert actual == expected, f"Log entry at line {i+1} does not match expected redaction.\nExpected: {expected}\nActual: {actual}"