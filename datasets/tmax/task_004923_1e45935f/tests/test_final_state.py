# test_final_state.py

import os
import subprocess
import pytest

def test_classifier_exists():
    classifier_path = "/home/user/classifier.py"
    assert os.path.exists(classifier_path), f"Classifier script is missing: {classifier_path}"
    assert os.path.isfile(classifier_path), f"Path is not a file: {classifier_path}"

def test_adversarial_corpus():
    evil_dir = "/app/hidden_corpus/evil/"
    clean_dir = "/app/hidden_corpus/clean/"
    classifier_path = "/home/user/classifier.py"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    clean_rejected = []

    for e_file in evil_files:
        result = subprocess.run(
            ["python3", classifier_path, e_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Evil files must be rejected (exit code 1)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(e_file))

    for c_file in clean_files:
        result = subprocess.run(
            ["python3", classifier_path, c_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Clean files must be preserved/accepted (exit code 0)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(c_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected: {', '.join(clean_rejected)}")

    if errors:
        pytest.fail(" | ".join(errors))