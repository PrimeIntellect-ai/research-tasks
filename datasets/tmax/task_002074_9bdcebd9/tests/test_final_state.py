# test_final_state.py

import os
import subprocess
import pytest

WRAPPER_SCRIPT = "/home/user/filter_wrapper.py"
VALIDATOR_BIN = "/app/log_validator"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"

def test_wrapper_script_exists_and_executable():
    assert os.path.exists(WRAPPER_SCRIPT), f"Filter script not found at {WRAPPER_SCRIPT}"
    assert os.path.isfile(WRAPPER_SCRIPT), f"Path {WRAPPER_SCRIPT} is not a file"
    assert os.access(WRAPPER_SCRIPT, os.X_OK), f"Filter script at {WRAPPER_SCRIPT} is not executable"

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, "rb") as f:
            original_content = f.read()

        try:
            result = subprocess.run(
                [WRAPPER_SCRIPT],
                input=original_content,
                capture_output=True,
                timeout=5
            )
            if result.stdout != original_content:
                modified_files.append(filename)
        except Exception as e:
            modified_files.append(f"{filename} (error: {e})")

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files modified/failed. Offending files: {', '.join(modified_files[:10])}"

def test_evil_corpus_sanitized():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, "rb") as f:
            original_content = f.read()

        try:
            # Run the wrapper script
            wrapper_result = subprocess.run(
                [WRAPPER_SCRIPT],
                input=original_content,
                capture_output=True,
                timeout=5
            )

            # Feed the output to the validator binary
            validator_result = subprocess.run(
                [VALIDATOR_BIN],
                input=wrapper_result.stdout,
                capture_output=True,
                timeout=5
            )

            # If the validator crashes (e.g., negative return code from signal, or non-zero exit indicating abort)
            if validator_result.returncode != 0:
                bypassed_files.append(filename)

        except Exception as e:
            bypassed_files.append(f"{filename} (error: {e})")

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the filter and crashed the validator. Offending files: {', '.join(bypassed_files[:10])}"