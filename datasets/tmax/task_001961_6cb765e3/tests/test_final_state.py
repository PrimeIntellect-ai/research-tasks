# test_final_state.py
import os
import subprocess
import pytest

def test_sanitiser_exists_and_executable():
    sanitiser_path = "/home/user/sanitiser"
    assert os.path.exists(sanitiser_path), f"Sanitiser executable not found at {sanitiser_path}"
    assert os.path.isfile(sanitiser_path), f"{sanitiser_path} is not a file"
    assert os.access(sanitiser_path, os.X_OK), f"Sanitiser at {sanitiser_path} is not executable"

def test_adversarial_corpus():
    sanitiser_path = "/home/user/sanitiser"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.xar2')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.xar2')]

    assert len(clean_files) > 0, "No clean corpus files found to test."
    assert len(evil_files) > 0, "No evil corpus files found to test."

    clean_rejected = []
    evil_bypassed = []

    for cf in clean_files:
        result = subprocess.run([sanitiser_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([sanitiser_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)