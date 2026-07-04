# test_final_state.py

import os
import stat
import json

def test_bare_git_repo():
    repo_path = "/home/user/edge-firmware.git"
    assert os.path.isdir(repo_path), f"Git repository directory not found at {repo_path}"

    config_path = os.path.join(repo_path, "config")
    assert os.path.isfile(config_path), f"Git config not found at {config_path}"

    with open(config_path, "r") as f:
        config_content = f.read()

    assert "bare = true" in config_content.lower(), f"Repository at {repo_path} is not configured as a bare repository."

def test_staging_permissions():
    staged_file = "/home/user/deploy_staging/firmware.json"
    assert os.path.isfile(staged_file), f"Staged file not found at {staged_file}"

    st = os.stat(staged_file)
    permissions = stat.S_IMODE(st.st_mode)

    assert permissions == 0o600, f"Permissions on {staged_file} are {oct(permissions)}, expected 0o600"

def test_device_update_log():
    log_file = "/home/user/device_update.log"
    assert os.path.isfile(log_file), f"Device update log not found at {log_file}. pexpect interaction may have failed."

    source_file = "/home/user/source_code/firmware.json"
    assert os.path.isfile(source_file), f"Source file missing at {source_file}"

    with open(source_file, "r") as f:
        source_content = f.read().strip()

    with open(log_file, "r") as f:
        log_content = f.read().strip()

    # We expect the payload in device_update.log to be the exact single line string of firmware.json
    assert log_content == source_content, f"Payload in {log_file} does not match the source firmware.json"

def test_email_outbox():
    outbox_file = "/home/user/email_outbox.log"
    assert os.path.isfile(outbox_file), f"Email outbox log not found at {outbox_file}. Email was not sent."

    with open(outbox_file, "r") as f:
        outbox_content = f.read()

    assert "deploybot@edge.local" in outbox_content, "Sender 'deploybot@edge.local' not found in email outbox log."
    assert "alerts@edge.local" in outbox_content, "Recipient 'alerts@edge.local' not found in email outbox log."
    assert "The firmware was successfully updated" in outbox_content, "Expected success message not found in email body."