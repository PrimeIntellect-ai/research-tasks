# test_final_state.py

import os
import json
import tarfile
import gzip
import pytest

SCRIPT_PATH = "/home/user/smart_archiver.py"
STATE_FILE = "/home/user/state.json"
FULL_BACKUP = "/home/user/full_backup.tar"
INCR_BACKUP = "/home/user/incr_backup.tar"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_state_file_validity_and_keys():
    assert os.path.isfile(STATE_FILE), f"The state file {STATE_FILE} does not exist."

    with open(STATE_FILE, 'r') as f:
        try:
            state = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The state file {STATE_FILE} is not valid JSON.")

    expected_keys = {
        'src/main.py', 
        'src/new_module.py', 
        'logs/server.log', 
        'logs/debug.txt', 
        'data/config.json'
    }

    # Normalize keys by stripping leading './' or '/' just in case, and match suffix
    actual_keys = set()
    for k in state.keys():
        normalized = k.lstrip('./').lstrip('/')
        # If the script stored absolute paths instead of relative, we extract the relative part
        if "project_workspace/" in normalized:
            normalized = normalized.split("project_workspace/")[-1]
        actual_keys.add(normalized)

    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"State file is missing expected keys: {missing_keys}"

def test_full_backup_contents():
    assert os.path.isfile(FULL_BACKUP), f"Full backup archive {FULL_BACKUP} does not exist."

    with tarfile.open(FULL_BACKUP, 'r') as tar:
        members = [m for m in tar.getmembers() if m.isfile()]
        names = set()
        for m in members:
            normalized = m.name.lstrip('./').lstrip('/')
            if "project_workspace/" in normalized:
                normalized = normalized.split("project_workspace/")[-1]
            names.add(normalized)

        expected_full = {
            'src/main.py', 
            'logs/server.log.gz', 
            'logs/debug.txt.gz', 
            'data/config.json'
        }

        assert expected_full == names, f"Full backup contents incorrect. Expected {expected_full}, got {names}"

def test_incremental_backup_contents():
    assert os.path.isfile(INCR_BACKUP), f"Incremental backup archive {INCR_BACKUP} does not exist."

    with tarfile.open(INCR_BACKUP, 'r') as tar:
        members = [m for m in tar.getmembers() if m.isfile()]
        names = set()
        for m in members:
            normalized = m.name.lstrip('./').lstrip('/')
            if "project_workspace/" in normalized:
                normalized = normalized.split("project_workspace/")[-1]
            names.add(normalized)

        expected_incr = {
            'src/new_module.py', 
            'logs/server.log.gz'
        }

        assert expected_incr == names, f"Incremental backup contents incorrect. Expected {expected_incr}, got {names}"

def test_incremental_backup_compressed_content():
    assert os.path.isfile(INCR_BACKUP), f"Incremental backup archive {INCR_BACKUP} does not exist."

    found = False
    with tarfile.open(INCR_BACKUP, 'r') as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith('server.log.gz'):
                found = True
                f = tar.extractfile(member)
                assert f is not None, "Failed to extract server.log.gz from the archive."
                try:
                    content = gzip.decompress(f.read()).decode('utf-8')
                except gzip.BadGzipFile:
                    pytest.fail("The file server.log.gz in the archive is not a valid gzip file.")

                assert "ERROR: Connection timeout" in content, "Compressed log file did not contain the updated text 'ERROR: Connection timeout'."

    assert found, "server.log.gz was not found in the incremental backup archive."