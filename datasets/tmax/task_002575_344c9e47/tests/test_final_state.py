# test_final_state.py

import os
import subprocess
import urllib.request
import pytest

def test_nginx_authorization_header():
    """
    Verifies that Nginx properly forwards the Authorization header to the backend.
    """
    url = "http://localhost:8080/api"
    test_token = "Bearer test_token_12345_secret"
    headers = {"Authorization": test_token}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200 from backend, got {response.status}"
            body = response.read().decode('utf-8')
            # The backend echoes headers. We check if our token made it through.
            assert test_token in body or "test_token_12345_secret" in body, \
                "Authorization header was not found in the backend response. Nginx is likely still stripping it."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect or retrieve valid response through Nginx: {e}")

def test_filter_script_adversarial_corpus():
    """
    Verifies the filter script correctly rejects evil JWTs and accepts clean JWTs.
    """
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (expected exit code 1)
    for filepath in evil_files:
        result = subprocess.run([script_path, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(filepath))

    # Test clean corpus (expected exit code 0)
    for filepath in clean_files:
        result = subprocess.run([script_path, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(filepath))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))