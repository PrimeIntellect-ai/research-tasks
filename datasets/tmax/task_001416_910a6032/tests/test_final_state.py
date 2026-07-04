# test_final_state.py

import os
import subprocess
import pytest

CLI_PATH = "/home/user/polyglot-sanitizer/bin/sanitizer_cli"
ORACLE_PATH = "/app/sanitizer_oracle"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_cli_binary_exists():
    assert os.path.isfile(CLI_PATH), f"Compiled binary not found at {CLI_PATH}"
    assert os.access(CLI_PATH, os.X_OK), f"Binary at {CLI_PATH} is not executable"

def test_adversarial_corpus():
    if not os.path.isfile(CLI_PATH):
        pytest.fail(f"Cannot run corpus tests: {CLI_PATH} is missing.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for filename in evil_files:
        file_path = os.path.join(EVIL_CORPUS, filename)
        result = subprocess.run([CLI_PATH, file_path], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(filename)

    # Test clean corpus
    for filename in clean_files:
        file_path = os.path.join(CLEAN_CORPUS, filename)

        oracle_result = subprocess.run([ORACLE_PATH, file_path], capture_output=True)
        cli_result = subprocess.run([CLI_PATH, file_path], capture_output=True)

        if cli_result.returncode != 0:
            clean_modified.append(f"{filename} (rejected with exit code {cli_result.returncode})")
        elif cli_result.stdout != oracle_result.stdout:
            clean_modified.append(f"{filename} (stdout mismatch)")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))