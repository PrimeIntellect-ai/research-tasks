# test_final_state.py

import os
import subprocess
import pytest

def test_filter_executable_exists():
    """Verify that the compiled C program exists and is executable."""
    executable_path = "/home/user/filter"
    assert os.path.isfile(executable_path), f"Expected executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_adversarial_corpus():
    """
    Run the filter executable against the clean and evil corpora.
    Clean files must return exit code 0.
    Evil files must return exit code 1.
    """
    executable_path = "/home/user/filter"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.nc')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.nc')]

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        result = subprocess.run([executable_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([executable_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))