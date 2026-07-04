# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import re
import pytest

def is_malicious(line):
    # Check for HTML/XML tags
    if re.search(r'<[^>]+>', line):
        return True
    # Check for javascript:
    if 'javascript:' in line.lower():
        return True
    # Check for unbalanced braces
    if line.count('{') != line.count('}'):
        return True
    return False

def test_worker_conf_exists_and_correct():
    conf_path = "/home/user/services/worker.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "REDIS_PORT=6379" in content, "REDIS_PORT=6379 not found in worker.conf"
    assert "API_ENDPOINT=http://localhost:5000" in content, "API_ENDPOINT=http://localhost:5000 not found in worker.conf"

def test_services_running():
    # Check if Flask is running and connected to Redis
    try:
        req = urllib.request.Request("http://localhost:5000/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            assert status == 200, f"Flask health endpoint returned status {status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Flask API at localhost:5000: {e}")

def test_filter_clean_corpus():
    clean_dir = "/home/user/corpora/clean/"
    assert os.path.isdir(clean_dir), "Clean corpus directory missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert clean_files, "No CSV files found in clean corpus"

    failed_files = []
    for filepath in clean_files:
        with open(filepath, 'r') as f:
            original_lines = f.read().splitlines()

        result = subprocess.run(['bash', '/home/user/filter.sh', filepath], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        # Clean corpus should be 100% preserved
        if len(output_lines) != len(original_lines):
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified. Offending files: {', '.join(failed_files)}")

def test_filter_evil_corpus():
    evil_dir = "/home/user/corpora/evil/"
    assert os.path.isdir(evil_dir), "Evil corpus directory missing"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert evil_files, "No CSV files found in evil corpus"

    failed_files = []
    for filepath in evil_files:
        with open(filepath, 'r') as f:
            original_lines = f.read().splitlines()

        result = subprocess.run(['bash', '/home/user/filter.sh', filepath], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()

        # Find all malicious lines in the original file
        malicious_original = [line for line in original_lines if is_malicious(line)]

        # Check if any malicious line made it to the output
        bypassed = [line for line in output_lines if is_malicious(line)]

        if bypassed:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")