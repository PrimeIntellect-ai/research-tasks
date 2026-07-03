# test_final_state.py
import os
import subprocess
import json
import urllib.request
import urllib.error
import glob
import pytest

def test_backup_exists():
    backup_path = "/home/user/backup/sshd_config.bak"
    assert os.path.isfile(backup_path), f"Backup file missing: {backup_path}"

def test_key_auditor_corpus():
    auditor_script = "/home/user/key_auditor.py"
    assert os.path.isfile(auditor_script), f"Key auditor script missing: {auditor_script}"

    evil_corpus = glob.glob("/app/corpus/evil/*.pub")
    clean_corpus = glob.glob("/app/corpus/clean/*.pub")

    assert len(evil_corpus) > 0, "Evil corpus is empty"
    assert len(clean_corpus) > 0, "Clean corpus is empty"

    evil_bypassed = []
    for evil_key in evil_corpus:
        result = subprocess.run(["python3", auditor_script, evil_key], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_key))

    clean_modified = []
    for clean_key in clean_corpus:
        result = subprocess.run(["python3", auditor_script, clean_key], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_key))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_corpus)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_corpus)} clean modified: {', '.join(clean_modified)}")

    assert not error_msg, " | ".join(error_msg)

def test_services_running():
    # Test internal API directly
    try:
        req = urllib.request.urlopen("http://127.0.0.1:5000/status", timeout=2)
        data = json.loads(req.read().decode())
        assert data.get("status") == "ok", "API on 5000 returned unexpected status"
    except Exception as e:
        pytest.fail(f"Could not reach Flask API on 127.0.0.1:5000: {e}")

    # Test SSH daemon
    result = subprocess.run(["nc", "-z", "127.0.0.1", "2222"])
    assert result.returncode == 0, "SSH daemon is not listening on 127.0.0.1:2222"

def test_keys_generated():
    host_key = "/home/user/bastion/ssh_host_ed25519_key"
    user_key = "/home/user/.ssh/id_ed25519"
    auth_keys = "/home/user/.ssh/authorized_keys"

    assert os.path.isfile(host_key), f"Host key missing: {host_key}"
    assert os.path.isfile(user_key), f"User private key missing: {user_key}"
    assert os.path.isfile(auth_keys), f"Authorized keys missing: {auth_keys}"

def test_ssh_tunnel_and_log():
    # Check the log file
    log_path = "/home/user/api_status.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
        try:
            data = json.loads(content)
            assert data.get("service") == "internal_api", "Log file does not contain expected API response"
        except json.JSONDecodeError:
            pytest.fail("Log file does not contain valid JSON")

    # Check the live tunnel
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/status", timeout=2)
        data = json.loads(req.read().decode())
        assert data.get("status") == "ok", "API via tunnel on 8080 returned unexpected status"
    except Exception as e:
        pytest.fail(f"Could not reach API via SSH tunnel on 127.0.0.1:8080: {e}")