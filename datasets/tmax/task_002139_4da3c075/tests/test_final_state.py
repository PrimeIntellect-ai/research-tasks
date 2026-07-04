# test_final_state.py

import os
import glob
import subprocess
import json
import pytest

def test_app_py_fixed():
    """Verify that the Flask app configuration has been corrected."""
    app_path = "/home/user/portal/app.py"
    assert os.path.exists(app_path), f"File missing: {app_path}"

    with open(app_path, "r") as f:
        content = f.read()

    # Check for Redis port fix
    assert "6379" in content, "app.py does not contain the corrected Redis port (6379)."
    assert "6380" not in content, "app.py still contains the incorrect Redis port (6380)."

    # Check for Nginx URL fix
    assert "http://127.0.0.1:8080/datasets/" in content, "app.py does not contain the corrected Nginx URL (http://127.0.0.1:8080/datasets/)."

def test_integration_log():
    """Verify that the integration test was run and produced the expected JSON output."""
    log_path = "/home/user/integration_test.log"
    assert os.path.exists(log_path), f"Integration test log missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content, "Integration test log is empty."

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"integration_test.log does not contain valid JSON. Content: {content}")

    assert data.get("returncode") == 0, f"Expected returncode 0 in integration log, got: {data.get('returncode')}"
    assert data.get("status") == "CLEAN", f"Expected status 'CLEAN' in integration log, got: {data.get('status')}"

def test_sanitizer_adversarial_corpus():
    """
    Verify the sanitizer script against the adversarial corpus.
    Must accept all clean datasets and reject all evil datasets.
    """
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.exists(sanitizer_path), f"Sanitizer script missing at {sanitizer_path}"

    clean_dirs = glob.glob("/home/user/corpora/clean/*")
    evil_dirs = glob.glob("/home/user/corpora/evil/*")

    assert len(clean_dirs) > 0, "No clean datasets found in /home/user/corpora/clean/"
    assert len(evil_dirs) > 0, "No evil datasets found in /home/user/corpora/evil/"

    clean_failures = []
    evil_failures = []

    # Test clean corpus
    for d in clean_dirs:
        res = subprocess.run(["python3", sanitizer_path, d], capture_output=True, text=True)
        out = res.stdout.strip()
        if out != "CLEAN" or res.returncode != 0:
            clean_failures.append(os.path.basename(d))

    # Test evil corpus
    for d in evil_dirs:
        res = subprocess.run(["python3", sanitizer_path, d], capture_output=True, text=True)
        out = res.stdout.strip()
        if out != "LEAK_DETECTED" or res.returncode != 1:
            evil_failures.append(os.path.basename(d))

    # Compile failure messages
    msg = []
    if evil_failures:
        msg.append(f"{len(evil_failures)} of {len(evil_dirs)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        msg.append(f"{len(clean_failures)} of {len(clean_dirs)} clean modified/rejected: {', '.join(clean_failures)}")

    if msg:
        pytest.fail(" | ".join(msg))