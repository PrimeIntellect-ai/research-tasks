# test_final_state.py

import os
import subprocess
import pytest

def test_binary_compiled():
    binary_path = "/app/vendored/xsv-0.13.0/target/release/xsv"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_sanitize_script_exists():
    script_path = "/home/user/sanitize_feed.sh"
    assert os.path.isfile(script_path), f"Sanitize script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Sanitize script at {script_path} is not executable"

def test_sanitize_script_empty_file():
    script_path = "/home/user/sanitize_feed.sh"
    # Create an empty file
    empty_file = "/tmp/empty.csv"
    open(empty_file, 'w').close()

    result = subprocess.run([script_path, empty_file], capture_output=True)
    assert result.returncode == 1, "Script should exit with code 1 for empty files"

    result_missing = subprocess.run([script_path, "/tmp/does_not_exist.csv"], capture_output=True)
    assert result_missing.returncode == 1, "Script should exit with code 1 for missing files"

def test_sanitize_script_adversarial_corpus():
    script_path = "/home/user/sanitize_feed.sh"
    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    # Check clean corpus
    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if f.endswith('.csv')]
    clean_failures = []

    for cf in clean_files:
        with open(cf, 'r') as f:
            expected_output = f.read()

        result = subprocess.run([script_path, cf], capture_output=True, text=True)
        if result.returncode != 0:
            clean_failures.append(f"{os.path.basename(cf)} (non-zero exit)")
            continue

        if result.stdout != expected_output:
            clean_failures.append(f"{os.path.basename(cf)} (modified)")

    # Check evil corpus
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if f.endswith('.csv')]
    evil_failures = []

    for ef in evil_files:
        with open(ef, 'r') as f:
            lines = f.readlines()

        expected_lines = [line for line in lines if "__PANIC_UNWRAP_TRIGGER__" not in line]
        expected_output = "".join(expected_lines)

        result = subprocess.run([script_path, ef], capture_output=True, text=True)
        if result.returncode != 0:
            evil_failures.append(f"{os.path.basename(ef)} (non-zero exit)")
            continue

        if result.stdout != expected_output:
            evil_failures.append(f"{os.path.basename(ef)} (bypassed or incorrectly modified)")

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))