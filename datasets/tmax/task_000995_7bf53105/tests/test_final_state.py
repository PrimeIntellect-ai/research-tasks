# test_final_state.py

import os
import shutil
import subprocess
import pytest

def test_classifier_exists():
    classifier_path = "/home/user/classifier.py"
    assert os.path.exists(classifier_path), f"Missing classifier script at {classifier_path}"
    assert os.path.isfile(classifier_path), f"{classifier_path} is not a file"

def test_adversarial_corpus_classification():
    classifier_path = "/home/user/classifier.py"
    mixed_dir = "/eval/corpus/mixed/"
    evil_dir = "/eval/corpus/evil/"
    clean_dir = "/eval/corpus/clean/"

    safe_out_dir = "/tmp/safe/"
    unsafe_out_dir = "/tmp/unsafe/"

    # Ensure output directories exist and are empty
    for d in [safe_out_dir, unsafe_out_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # Run the agent's classifier
    cmd = ["python3", classifier_path, mixed_dir, safe_out_dir, unsafe_out_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Classifier script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Gather expected files
    expected_evil = set(os.listdir(evil_dir)) if os.path.exists(evil_dir) else set()
    expected_clean = set(os.listdir(clean_dir)) if os.path.exists(clean_dir) else set()

    # Gather actual files
    actual_unsafe = set(os.listdir(unsafe_out_dir))
    actual_safe = set(os.listdir(safe_out_dir))

    # Check evil files
    evil_bypassed = expected_evil - actual_unsafe
    evil_total = len(expected_evil)

    # Check clean files
    clean_modified = expected_clean - actual_safe
    clean_total = len(expected_clean)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {evil_total} evil bypassed: {', '.join(sorted(evil_bypassed))}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {clean_total} clean modified (or rejected): {', '.join(sorted(clean_modified))}")

    if errors:
        pytest.fail(" | ".join(errors))