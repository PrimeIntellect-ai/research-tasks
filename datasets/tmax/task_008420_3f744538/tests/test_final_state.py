# test_final_state.py

import os
import json
import pytest

MANIFEST_PATH = "/home/user/manifests/vms.json"
BACKUP_PATH = "/home/user/backup/vms.json.bak"
RUNNERS_DIR = "/home/user/runners"
LOG_PATH = "/home/user/operator_state.log"

def test_backup_created_and_identical():
    assert os.path.exists(BACKUP_PATH), f"Backup file {BACKUP_PATH} does not exist"
    assert os.path.exists(MANIFEST_PATH), f"Original manifest {MANIFEST_PATH} is missing"

    with open(MANIFEST_PATH, 'r') as f_orig, open(BACKUP_PATH, 'r') as f_bak:
        orig_content = f_orig.read()
        bak_content = f_bak.read()

    assert orig_content == bak_content, "Backup content does not match the original manifest"

def test_web_server_runner():
    runner_path = os.path.join(RUNNERS_DIR, "web-server.sh")
    assert os.path.exists(runner_path), f"Runner script {runner_path} does not exist"
    assert os.access(runner_path, os.X_OK), f"Runner script {runner_path} is not executable"

    with open(runner_path, 'r') as f:
        content = f.read().strip()

    expected_command = "qemu-system-x86_64 -m 2G -hda /home/user/images/web.img -vnc :1"
    assert content == expected_command, f"Incorrect content in {runner_path}. Expected: '{expected_command}', but got: '{content}'"

def test_db_server_runner():
    runner_path = os.path.join(RUNNERS_DIR, "db-server.sh")
    assert os.path.exists(runner_path), f"Runner script {runner_path} does not exist"
    assert os.access(runner_path, os.X_OK), f"Runner script {runner_path} is not executable"

    with open(runner_path, 'r') as f:
        content = f.read().strip()

    expected_command = "qemu-system-x86_64 -m 4G -hda /home/user/images/db.img -vnc :0"
    assert content == expected_command, f"Incorrect content in {runner_path}. Expected: '{expected_command}', but got: '{content}'"

def test_cache_server_runner_not_created():
    runner_path = os.path.join(RUNNERS_DIR, "cache-server.sh")
    assert not os.path.exists(runner_path), f"Runner script {runner_path} should not exist due to missing image"

def test_operator_state_log():
    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} does not exist"

    with open(LOG_PATH, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[SUCCESS] Created runner for web-server",
        "[SUCCESS] Created runner for db-server",
        "[ERROR] Missing image for cache-server"
    ]

    # We check if all expected lines are present. The order is expected to match the JSON array order.
    assert lines == expected_lines, f"Log file content is incorrect. Expected {expected_lines}, got {lines}"