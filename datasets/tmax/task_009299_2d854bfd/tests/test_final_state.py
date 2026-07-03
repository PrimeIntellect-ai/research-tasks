# test_final_state.py

import os
import stat
import hashlib
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/archive_worker.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_uses_flock():
    script_path = "/home/user/archive_worker.sh"
    with open(script_path, "r") as f:
        content = f.read()
    assert "flock" in content, "The script must use 'flock' to lock files."

def test_logs_truncated():
    logs = [
        "/home/user/active_logs/web.log",
        "/home/user/active_logs/db.log",
        "/home/user/active_logs/auth.log"
    ]
    for log in logs:
        assert os.path.isfile(log), f"Log file {log} is missing."
        assert os.path.getsize(log) == 0, f"Log file {log} was not truncated to 0 bytes."

def test_archives_created_and_valid():
    archives = [
        "/home/user/archived_logs/web.log.gz",
        "/home/user/archived_logs/db.log.gz",
        "/home/user/archived_logs/auth.log.gz"
    ]
    for archive in archives:
        assert os.path.isfile(archive), f"Archive {archive} does not exist."
        with open(archive, "rb") as f:
            magic = f.read(2)
        assert magic == b"\x1f\x8b", f"File {archive} is not a valid gzip file."

def test_manifest_contents():
    manifest_path = "/home/user/archived_logs/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    # Compute expected hashes
    web_data = b"Web log line 1: GET /index.html 200\nWeb log line 2: POST /login 401\n"
    web_hash = hashlib.sha256(web_data).hexdigest()

    db_data = b"Database connection established\n" + b"".join(f"DB query {i} executed\n".encode() for i in range(1, 101))
    db_hash = hashlib.sha256(db_data).hexdigest()

    auth_data = b"Auth failure: user admin from 192.168.1.50\nAuth success: user root from 10.0.0.5\n"
    auth_hash = hashlib.sha256(auth_data).hexdigest()

    with open(manifest_path, "r") as f:
        manifest_content = f.read()

    assert web_hash in manifest_content, f"Web log hash {web_hash} not found in manifest."
    assert "web.log" in manifest_content, "web.log filename not found in manifest."

    assert db_hash in manifest_content, f"DB log hash {db_hash} not found in manifest."
    assert "db.log" in manifest_content, "db.log filename not found in manifest."

    assert auth_hash in manifest_content, f"Auth log hash {auth_hash} not found in manifest."
    assert "auth.log" in manifest_content, "auth.log filename not found in manifest."