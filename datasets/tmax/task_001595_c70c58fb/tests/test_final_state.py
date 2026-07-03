# test_final_state.py

import os
import subprocess
import json
import urllib.request
import pytest
import glob

def test_services_running():
    """Test that the Nginx proxy correctly routes to the Flask API."""
    url = "http://localhost:8080/api/vector"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            expected_data = {"v_x": 0.5, "v_y": -0.5, "v_z": 1.0}
            assert data == expected_data, f"Expected {expected_data}, got {data}"
    except Exception as e:
        pytest.fail(f"Failed to reach API through Nginx proxy at {url}: {e}")

def test_filter_script_exists_and_executable():
    """Test that the filter script exists and is executable."""
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def get_redis_set_members(set_name):
    """Helper to get members of a Redis set using redis-cli."""
    try:
        result = subprocess.run(
            ["redis-cli", "smembers", set_name],
            capture_output=True, text=True, check=True
        )
        return set(result.stdout.split())
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis set {set_name}: {e.stderr}")

def test_adversarial_corpus():
    """Test the script against the clean and evil corpora."""
    script_path = "/home/user/filter.sh"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert clean_files, "No clean files found in corpus."
    assert evil_files, "No evil files found in corpus."

    clean_failures = []
    evil_failures = []

    # Test clean corpus
    for f in clean_files:
        basename = os.path.basename(f)
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(basename)

    # Test evil corpus
    for f in evil_files:
        basename = os.path.basename(f)
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(basename)

    # Check Redis sets
    accepted_files = get_redis_set_members("accepted_files")
    rejected_files = get_redis_set_members("rejected_files")

    for f in clean_files:
        basename = os.path.basename(f)
        if basename not in accepted_files and basename not in clean_failures:
            clean_failures.append(f"{basename} (missing from Redis accepted_files)")

    for f in evil_files:
        basename = os.path.basename(f)
        if basename not in rejected_files and basename not in evil_failures:
            evil_failures.append(f"{basename} (missing from Redis rejected_files)")

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))