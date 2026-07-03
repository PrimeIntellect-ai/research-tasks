# test_final_state.py

import os
import subprocess
import pytest

WRAPPER_PATH = "/home/user/sanitize_wrapper.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
BINARY_PATH = "/app/bin/spec_deconv"

def test_wrapper_exists_and_executable():
    assert os.path.exists(WRAPPER_PATH), f"Wrapper script not found at {WRAPPER_PATH}"
    assert os.path.isfile(WRAPPER_PATH), f"{WRAPPER_PATH} is not a file"
    assert os.access(WRAPPER_PATH, os.X_OK), f"Wrapper script at {WRAPPER_PATH} is not executable"

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus dir missing: {EVIL_CORPUS_DIR}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert evil_files, "No files found in evil corpus"

    bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        try:
            result = subprocess.run(
                [WRAPPER_PATH, filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 1 or result.stdout.strip() != "REJECT":
                bypassed.append(filename)
        except subprocess.TimeoutExpired:
            bypassed.append(f"{filename} (timeout)")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil files bypassed rejection. Offending files: {', '.join(bypassed)}")

def test_clean_corpus_preserved():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus dir missing: {CLEAN_CORPUS_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert clean_files, "No files found in clean corpus"

    modified_or_failed = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)

        # Get expected output from the binary directly
        expected_result = subprocess.run(
            [BINARY_PATH, filepath],
            capture_output=True,
            text=True,
            timeout=5
        )

        try:
            wrapper_result = subprocess.run(
                [WRAPPER_PATH, filepath],
                capture_output=True,
                text=True,
                timeout=5
            )

            if wrapper_result.returncode != 0:
                modified_or_failed.append(f"{filename} (exit code {wrapper_result.returncode})")
            elif wrapper_result.stdout.strip() == "REJECT":
                modified_or_failed.append(f"{filename} (falsely rejected)")
            elif wrapper_result.stdout != expected_result.stdout:
                modified_or_failed.append(f"{filename} (stdout mismatch)")

        except subprocess.TimeoutExpired:
            modified_or_failed.append(f"{filename} (timeout)")

    if modified_or_failed:
        pytest.fail(f"{len(modified_or_failed)} of {len(clean_files)} clean files failed or modified. Offending files: {', '.join(modified_or_failed)}")