# test_final_state.py

import os
import subprocess
import re
import pytest

SCRIPT_PATH = "/home/user/redact.sh"
AUDIT_TRAIL_PATH = "/home/user/audit_trail.txt"
EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"

def python_redact(text):
    # Redact AWS Access Keys
    text = re.sub(r'AKIA[A-Z0-9]{16}', '[REDACTED_AWS]', text)
    # Redact URL Credentials
    text = re.sub(r'(https?://[^:\s@/]+:)([^:@\s/]+)(@)', r'\g<1>[REDACTED_CREDS]\3', text)
    return text

def run_script(file_path):
    result = subprocess.run(
        ["/bin/bash", SCRIPT_PATH, file_path],
        capture_output=True,
        text=True
    )
    return result.stdout

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Redaction script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_audit_trail_exists_and_redacted():
    assert os.path.exists(AUDIT_TRAIL_PATH), f"Audit trail not found at {AUDIT_TRAIL_PATH}"
    with open(AUDIT_TRAIL_PATH, "r") as f:
        content = f.read()

    assert "[REDACTED_CREDS]" in content, "Audit trail missing [REDACTED_CREDS]"
    assert "[REDACTED_AWS]" in content, "Audit trail missing [REDACTED_AWS]"
    assert "supersecret99" not in content, "Audit trail still contains the URL password"
    assert "AKIAIOSFODNN7EXAMPLE" not in content, "Audit trail still contains the AWS key"

def test_clean_corpus():
    if not os.path.exists(CLEAN_DIR):
        pytest.skip("Clean corpus dir missing")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    modified_files = []

    for cf in clean_files:
        with open(cf, "r") as f:
            original = f.read()
        output = run_script(cf)
        if output != original:
            modified_files.append(os.path.basename(cf))

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}"

def test_evil_corpus():
    if not os.path.exists(EVIL_DIR):
        pytest.skip("Evil corpus dir missing")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    bypassed_files = []

    for ef in evil_files:
        with open(ef, "r") as f:
            original = f.read()
        expected = python_redact(original)
        output = run_script(ef)

        # Check if any secrets are still left or if it doesn't match expected
        if re.search(r'AKIA[A-Z0-9]{16}', output) or re.search(r'https?://[^:\s@/]+:[^:@\s/]+@', output):
            bypassed_files.append(os.path.basename(ef))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"