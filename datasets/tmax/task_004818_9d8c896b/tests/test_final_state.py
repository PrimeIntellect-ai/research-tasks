# test_final_state.py

import os
import sys
import json
import urllib.request
import urllib.error
import glob
import subprocess
import pytest

WAF_DIR = "/home/user/waf"
NGINX_CONF = "/home/user/gateway/nginx.conf"
EVIL_CORPUS = "/app/corpus/evil"
CLEAN_CORPUS = "/app/corpus/clean"

def test_validator_corpus():
    sys.path.append(WAF_DIR)
    try:
        from validator import is_clean
    except ImportError:
        pytest.fail(f"Could not import is_clean from {WAF_DIR}/validator.py")

    evil_files = glob.glob(os.path.join(EVIL_CORPUS, "*.json"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS, "*.json"))

    if not evil_files or not clean_files:
        pytest.fail("Corpus files are missing. Cannot validate.")

    evil_bypassed = []
    for fpath in evil_files:
        with open(fpath, "r") as f:
            payload = f.read()
        try:
            if is_clean(payload) is not False:
                evil_bypassed.append(os.path.basename(fpath))
        except Exception:
            # If it crashes on evil, it's not strictly 'False', but maybe they didn't catch JSONDecodeError.
            # The spec says "return False if malicious or malformed". So it must return False, not raise.
            evil_bypassed.append(os.path.basename(fpath) + " (raised exception)")

    clean_modified = []
    for fpath in clean_files:
        with open(fpath, "r") as f:
            payload = f.read()
        try:
            if is_clean(payload) is not True:
                clean_modified.append(os.path.basename(fpath))
        except Exception:
            clean_modified.append(os.path.basename(fpath) + " (raised exception)")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_nginx_config_updated():
    assert os.path.exists(NGINX_CONF), "nginx.conf missing"
    with open(NGINX_CONF, "r") as f:
        content = f.read()
    assert "127.0.0.1:8081" in content, "Nginx config not updated to point to WAF proxy on port 8081"
    assert "127.0.0.1:5000" not in content, "Nginx config still points to Flask backend on port 5000"

def test_git_repo_and_hook():
    git_dir = os.path.join(WAF_DIR, ".git")
    assert os.path.isdir(git_dir), f"Git repository not initialized in {WAF_DIR}"

    hook_path = os.path.join(git_dir, "hooks", "post-commit")
    assert os.path.isfile(hook_path), "post-commit hook not found"
    assert os.access(hook_path, os.X_OK), "post-commit hook is not executable"

def test_end_to_end_proxy():
    clean_payload = json.dumps({"device_id": "sensor-01A", "readings": {"temp": 25.4, "humidity": 60}}).encode('utf-8')
    evil_payload = json.dumps({"device_id": "drop table;", "readings": {}}).encode('utf-8')

    req_clean = urllib.request.Request("http://127.0.0.1:8080/telemetry", data=clean_payload, method="POST")
    req_clean.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req_clean, timeout=2) as response:
            assert response.status == 200, "Clean payload did not return 200 OK"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to route clean payload through Nginx: {e}")

    req_evil = urllib.request.Request("http://127.0.0.1:8080/telemetry", data=evil_payload, method="POST")
    req_evil.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req_evil, timeout=2) as response:
            pytest.fail(f"Evil payload was not blocked, returned {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Evil payload returned {e.code} instead of 403 Forbidden"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to route evil payload through Nginx: {e}")