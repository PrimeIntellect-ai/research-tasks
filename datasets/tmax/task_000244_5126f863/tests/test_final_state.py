# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_fixed():
    """Verify that Nginx proxy is fixed and returns 200 OK with 'OK'."""
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8080/health", timeout=5)
        content = response.read().decode('utf-8').strip()
        assert response.getcode() == 200, f"Expected HTTP 200, got {response.getcode()}"
        assert content == "OK", f"Expected response content 'OK', got '{content}'"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Nginx still returning error: HTTP {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx: {e}")

def test_waf_script_adversarial_corpus():
    """Verify that waf.sh correctly rejects evil payloads and accepts clean payloads."""
    waf_path = "/home/user/waf.sh"
    assert os.path.isfile(waf_path), f"WAF script {waf_path} does not exist"
    assert os.access(waf_path, os.X_OK), f"WAF script {waf_path} is not executable"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil files found in corpus"
    assert len(clean_files) > 0, "No clean files found in corpus"

    evil_bypassed = []
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        result = subprocess.run([waf_path, filepath], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            evil_bypassed.append(f)

    clean_modified = []
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        result = subprocess.run([waf_path, filepath], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))