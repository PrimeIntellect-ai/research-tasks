# test_final_state.py

import os
import subprocess
import pytest

def test_services_running_and_proxying():
    """
    Validates that the Nginx proxy is properly configured, running, 
    and proxying requests to the backend over HTTPS.
    """
    try:
        result = subprocess.run(
            ["curl", "-s", "-k", "https://127.0.0.1:8443/"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Timeout while trying to connect to Nginx on https://127.0.0.1:8443/")
    except FileNotFoundError:
        pytest.fail("curl command not found")

    assert result.returncode == 0, f"curl failed to connect to the reverse proxy. Return code: {result.returncode}, Stderr: {result.stderr}"
    assert "BACKEND_OK" in result.stdout, f"Expected 'BACKEND_OK' from the backend, but got: {result.stdout}"

def test_filter_script_adversarial_corpus():
    """
    Validates the filter.sh script against the clean and evil corpora.
    Clean paths should exit with 0.
    Evil paths should exit with != 0.
    """
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Filter script not found at {script_path}"

    clean_corpus_path = "/app/corpus/clean.txt"
    evil_corpus_path = "/app/corpus/evil.txt"

    assert os.path.isfile(clean_corpus_path), f"Clean corpus missing at {clean_corpus_path}"
    assert os.path.isfile(evil_corpus_path), f"Evil corpus missing at {evil_corpus_path}"

    with open(clean_corpus_path, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    with open(evil_corpus_path, "r") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    clean_failures = []
    for line in clean_lines:
        result = subprocess.run(["bash", script_path, line], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(line)

    evil_failures = []
    for line in evil_lines:
        result = subprocess.run(["bash", script_path, line], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(line)

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_lines)} clean modified/rejected: {clean_failures}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_lines)} evil bypassed/accepted: {evil_failures}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))