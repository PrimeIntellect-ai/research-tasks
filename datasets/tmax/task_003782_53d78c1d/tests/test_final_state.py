# test_final_state.py

import os
import subprocess
import pytest

def test_nginx_config_fixed():
    """Verify that the Nginx configuration syntax error has been fixed."""
    proc = subprocess.run(['nginx', '-t'], capture_output=True)
    assert proc.returncode == 0, f"Nginx config syntax check failed. It is still broken:\n{proc.stderr.decode(errors='ignore')}"

def test_log_ingest_script_fixed():
    """Verify that log_ingest.sh has been updated to use the correct Redis port and integrate the sanitizer."""
    ingest_script_path = "/app/log_ingest.sh"
    assert os.path.isfile(ingest_script_path), f"{ingest_script_path} does not exist"

    with open(ingest_script_path, "r") as f:
        content = f.read()

    assert "6379" in content, "log_ingest.sh does not contain the correct redis-cli port 6379."
    assert "6380" not in content, "log_ingest.sh still contains the incorrect redis-cli port 6380."
    assert "sanitizer.sh" in content, "log_ingest.sh does not appear to pipe logs through sanitizer.sh."

def test_sanitizer_adversarial_corpus():
    """
    Verify that sanitizer.sh correctly filters the adversarial corpus.
    It must preserve 100% of clean logs and drop 100% of evil logs.
    """
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"
    sanitizer_path = "/app/sanitizer.sh"

    assert os.path.isfile(sanitizer_path), f"{sanitizer_path} does not exist"

    clean_modified = []
    clean_total = 0
    if os.path.isdir(clean_dir):
        for f in sorted(os.listdir(clean_dir)):
            filepath = os.path.join(clean_dir, f)
            if os.path.isfile(filepath):
                clean_total += 1
                with open(filepath, 'rb') as fd:
                    original = fd.read()

                proc = subprocess.run(['bash', sanitizer_path], input=original, capture_output=True)
                if proc.stdout != original:
                    clean_modified.append(f)

    evil_bypassed = []
    evil_total = 0
    if os.path.isdir(evil_dir):
        for f in sorted(os.listdir(evil_dir)):
            filepath = os.path.join(evil_dir, f)
            if os.path.isfile(filepath):
                evil_total += 1
                with open(filepath, 'rb') as fd:
                    original = fd.read()

                proc = subprocess.run(['bash', sanitizer_path], input=original, capture_output=True)
                # The output should be empty for evil lines
                if proc.stdout.strip() != b"":
                    evil_bypassed.append(f)

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {clean_total} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {evil_total} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail("Sanitizer failed corpus validation: " + "; ".join(errors))