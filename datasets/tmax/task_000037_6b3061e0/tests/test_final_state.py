# test_final_state.py

import os
import subprocess
import pytest

def test_token_filter_exists_and_executable():
    binary_path = "/home/user/token_filter"
    assert os.path.isfile(binary_path), f"Compiled binary is missing: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

def test_adversarial_corpus_classification():
    binary_path = "/home/user/token_filter"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory is missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory is missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run([binary_path, cf], capture_output=True)
        # Clean files should be ACCEPTED (exit code 0)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run([binary_path, ef], capture_output=True)
        # Evil files should be REJECTED (exit code 1)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))