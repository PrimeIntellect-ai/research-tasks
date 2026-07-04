# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_adversarial_corpus_verification():
    """
    Tests the /app/verify_manifest.py script against the clean and evil corpora.
    Ensures 100% of clean files are VALID and 100% of evil files are INVALID.
    """
    script_path = "/app/verify_manifest.py"
    clean_corpus_path = "/home/user/corpus/clean"
    evil_corpus_path = "/home/user/corpus/evil"

    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    clean_files = glob.glob(os.path.join(clean_corpus_path, "*.json"))
    evil_files = glob.glob(os.path.join(evil_corpus_path, "*.json"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_corpus_path}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_corpus_path}"

    clean_failed = []
    evil_failed = []

    # Test clean corpus
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", script_path, filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "VALID":
            clean_failed.append(os.path.basename(filepath))

    # Test evil corpus
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", script_path, filepath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "INVALID":
            evil_failed.append(os.path.basename(filepath))

    # Summarize failures
    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))