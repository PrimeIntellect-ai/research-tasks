# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_part1_nginx_flask_integration():
    """
    Test that Nginx and Flask are correctly configured and running.
    """
    # Start the services
    start_script = "/app/start.sh"
    assert os.path.isfile(start_script), f"{start_script} is missing"

    # Execute start.sh
    subprocess.run([start_script], check=True)

    # Give services a moment to start
    time.sleep(2)

    # Test /login -> 200
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/login")
        with urllib.request.urlopen(req) as response:
            assert response.getcode() == 200, "Expected HTTP 200 for /login"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to access /login: {e}")

    # Test /admin -> 403
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/admin")
        with urllib.request.urlopen(req) as response:
            pytest.fail("Expected HTTP 403 for /admin, but got 200")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected HTTP 403 for /admin, got {e.code}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to access /admin: {e}")

def test_part2_url_filter_script():
    """
    Test the url_filter.sh script against the adversarial corpus.
    """
    script_path = "/home/user/url_filter.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil corpus files found"
    assert len(clean_files) > 0, "No clean corpus files found"

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run([script_path, evil_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        with open(clean_file, "r") as f:
            expected_output = f.read().strip()

        result = subprocess.run([script_path, clean_file], capture_output=True, text=True)
        output = result.stdout.strip()

        if output != expected_output:
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))