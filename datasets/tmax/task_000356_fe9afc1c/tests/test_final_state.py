# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_psd_image_exists():
    """Check that the PSD image was generated."""
    path = "/home/user/psd.png"
    assert os.path.isfile(path), f"Missing PSD image file: {path}"

def test_classifier_exists_and_executable():
    """Check that the classifier exists and is executable."""
    path = "/home/user/classifier"
    assert os.path.isfile(path), f"Missing classifier executable: {path}"
    assert os.access(path, os.X_OK), f"Classifier is not executable: {path}"

def test_classifier_on_adversarial_corpus():
    """Check that the classifier correctly identifies clean and evil files."""
    classifier_path = "/home/user/classifier"
    clean_dir = "/app/verifier/clean"
    evil_dir = "/app/verifier/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.wav"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.wav"))

    assert len(clean_files) > 0, "No clean files found in verifier corpus."
    assert len(evil_files) > 0, "No evil files found in verifier corpus."

    failed_clean = []
    for f in clean_files:
        result = subprocess.run([classifier_path, f], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        result = subprocess.run([classifier_path, f], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(f))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean files incorrectly classified as evil (exit code != 0): {failed_clean[:5]}...")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed classification (exit code != 1): {failed_evil[:5]}...")

    if errors:
        pytest.fail("\n".join(errors))