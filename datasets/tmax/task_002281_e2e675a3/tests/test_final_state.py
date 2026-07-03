# test_final_state.py

import os
import pwd
import stat
import urllib.request
import urllib.error
import subprocess
import pytest
from pathlib import Path

def test_secure_data_permissions():
    crt_file = Path("/app/secure_data/server.crt")
    key_file = Path("/app/secure_data/server.key")

    assert crt_file.exists(), f"Missing file: {crt_file}"
    assert key_file.exists(), f"Missing file: {key_file}"

    try:
        www_data_uid = pwd.getpwnam("www-data").pw_uid
    except KeyError:
        pytest.fail("User 'www-data' does not exist")

    crt_stat = crt_file.stat()
    key_stat = key_file.stat()

    assert crt_stat.st_uid == www_data_uid, f"Expected {crt_file} to be owned by www-data"
    assert key_stat.st_uid == www_data_uid, f"Expected {key_file} to be owned by www-data"

    assert stat.S_IMODE(crt_stat.st_mode) == 0o444, f"Expected {crt_file} to have 0444 permissions"
    assert stat.S_IMODE(key_stat.st_mode) == 0o400, f"Expected {key_file} to have 0400 permissions"

def test_services_running_and_proxy_pass():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/api/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx or backend via Nginx: {e}")

def test_filter_binary_adversarial_corpus():
    filter_bin = Path("/home/user/filter")
    assert filter_bin.exists(), f"Missing filter binary: {filter_bin}"
    assert os.access(filter_bin, os.X_OK), f"Filter binary is not executable: {filter_bin}"

    clean_corpus = Path("/app/corpus/clean")
    evil_corpus = Path("/app/corpus/evil")

    assert clean_corpus.is_dir(), f"Missing clean corpus dir: {clean_corpus}"
    assert evil_corpus.is_dir(), f"Missing evil corpus dir: {evil_corpus}"

    clean_files = list(clean_corpus.glob("*"))
    evil_files = list(evil_corpus.glob("*"))

    clean_modified = []
    for f in clean_files:
        if not f.is_file():
            continue
        with open(f, "rb") as stdin_f:
            result = subprocess.run([str(filter_bin)], stdin=stdin_f, capture_output=True, text=True)
            # Clean files should be 100% ACCEPT
            if "REJECT" in result.stdout:
                clean_modified.append(f.name)

    evil_bypassed = []
    for f in evil_files:
        if not f.is_file():
            continue
        with open(f, "rb") as stdin_f:
            result = subprocess.run([str(filter_bin)], stdin=stdin_f, capture_output=True, text=True)
            # Evil files should contain at least one REJECT
            if "REJECT" not in result.stdout:
                evil_bypassed.append(f.name)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_verification_log_exists():
    ver_log = Path("/home/user/verification.log")
    assert ver_log.exists(), f"Missing verification log: {ver_log}"
    content = ver_log.read_text()
    assert "ACCEPT" in content or "REJECT" in content, "verification.log does not contain expected filter output"