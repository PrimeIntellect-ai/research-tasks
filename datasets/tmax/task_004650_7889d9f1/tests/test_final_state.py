# test_final_state.py

import os
import subprocess
import pytest

SANITIZER_BIN = "/home/user/sanitizer"
EVIL_DIR = "/opt/corpora/evil"
CLEAN_DIR = "/opt/corpora/clean"

def test_sanitizer_executable_exists():
    assert os.path.isfile(SANITIZER_BIN), f"Executable {SANITIZER_BIN} not found."
    assert os.access(SANITIZER_BIN, os.X_OK), f"{SANITIZER_BIN} is not executable."

def run_sanitizer(input_data: bytes) -> bytes:
    result = subprocess.run(
        [SANITIZER_BIN],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=5
    )
    return result.stdout

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert clean_files, "No clean corpus files found."

    modified_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, "rb") as f:
            input_data = f.read()

        output_data = run_sanitizer(input_data)

        if output_data != input_data:
            modified_files.append(filename)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files modified: {', '.join(modified_files)}"

def test_evil_corpus_redacted():
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert evil_files, "No evil corpus files found."

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        with open(filepath, "rb") as f:
            input_data = f.read()

        output_data = run_sanitizer(input_data)
        output_text = output_data.decode("utf-8", errors="replace")

        # Check for private keys
        has_private_key = (
            "BEGIN PRIVATE KEY" in output_text or 
            "BEGIN RSA PRIVATE KEY" in output_text or
            "END PRIVATE KEY" in output_text or
            "END RSA PRIVATE KEY" in output_text
        )

        # Check if weak hashes were redacted
        # The setup uses 'password' hash for admin. The output should have REDACTED.
        # We expect at least one REDACTED in the evil output since it contains weak passwords.
        # Also, the specific hash from evil_1.log should not be present.
        has_redacted = "REDACTED" in output_text

        # If it failed to redact private keys or failed to redact the weak password
        if has_private_key or not has_redacted:
            bypassed_files.append(filename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed_files)}"