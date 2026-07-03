# test_final_state.py

import os
import subprocess
import pytest

def test_filter_executable_exists():
    """Verify that the compiled Go program exists at the required location."""
    executable_path = "/home/user/filter"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_adversarial_corpus():
    """Run the filter on both clean and evil corpora and assert correct exit codes."""
    executable_path = "/home/user/filter"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failed = []
    for filepath in clean_files:
        result = subprocess.run([executable_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(filepath))

    evil_failed = []
    for filepath in evil_files:
        result = subprocess.run([executable_path, filepath], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(filepath))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean files rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil files bypassed: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))