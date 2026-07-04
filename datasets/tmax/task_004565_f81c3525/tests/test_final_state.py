# test_final_state.py

import os
import subprocess
import pytest

def test_extracted_password():
    """Verify that the leaked password was correctly extracted and decoded."""
    password_file = "/home/user/old_password.txt"
    assert os.path.isfile(password_file), f"Expected password file does not exist at {password_file}"

    with open(password_file, "r") as f:
        content = f.read().strip()

    expected_password = "sup3r_secret_1337"
    assert content == expected_password, f"Extracted password does not match. Expected '{expected_password}', but got '{content}'"

def test_detector_script_against_corpus():
    """Verify that the detector.py script correctly classifies evil and clean payloads."""
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), f"Detector script not found at {detector_script}"

    evil_corpus_dir = "/app/eval_corpus/evil/"
    clean_corpus_dir = "/app/eval_corpus/clean/"

    assert os.path.isdir(evil_corpus_dir), f"Evil evaluation corpus directory missing: {evil_corpus_dir}"
    assert os.path.isdir(clean_corpus_dir), f"Clean evaluation corpus directory missing: {clean_corpus_dir}"

    evil_files = [f for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]
    clean_files = [f for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus
    for filename in evil_files:
        filepath = os.path.join(evil_corpus_dir, filename)
        result = subprocess.run(
            ["python3", detector_script, filepath],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "EVIL":
            bypassed_evil.append(filename)

    # Test clean corpus
    for filename in clean_files:
        filepath = os.path.join(clean_corpus_dir, filename)
        result = subprocess.run(
            ["python3", detector_script, filepath],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "CLEAN":
            modified_clean.append(filename)

    # Compile failure message
    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    assert not error_messages, "Detector classification failed: " + " | ".join(error_messages)