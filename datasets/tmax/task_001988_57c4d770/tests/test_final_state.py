# test_final_state.py

import os
import glob
import subprocess

def test_deadlock_detector_binary_exists():
    """Check if the compiled Rust binary exists."""
    binary_path = "/home/user/app/deadlock_detector/target/debug/deadlock_detector"
    assert os.path.isfile(binary_path), f"Missing compiled Rust binary at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_adversarial_corpus():
    """Check if the binary correctly identifies clean and evil corpora."""
    binary_path = "/home/user/app/deadlock_detector/target/debug/deadlock_detector"
    clean_path = "/home/user/corpora/clean/*.csv"
    evil_path = "/home/user/corpora/evil/*.csv"

    clean_files = sorted(glob.glob(clean_path))
    evil_files = sorted(glob.glob(evil_path))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean files rejected (expected exit code 0): {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil files bypassed (expected exit code 1): {', '.join(evil_failed)}")

    assert not errors, "\n".join(errors)