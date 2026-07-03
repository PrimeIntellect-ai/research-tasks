# test_final_state.py
import os
import subprocess
import pytest

def test_sanitizer_exists():
    assert os.path.isfile("/home/user/sanitizer.py"), "Sanitizer script /home/user/sanitizer.py does not exist."

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), "Sanitizer script not found."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory at {evil_dir}"

    clean_files = os.listdir(clean_dir)
    evil_files = os.listdir(evil_dir)

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failed = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        # Pass the absolute path to test if the script correctly extracts the basename
        result = subprocess.run(
            ["python3", sanitizer_path, filepath],
            capture_output=True
        )
        # Clean files should be accepted (exit code 0)
        if result.returncode != 0:
            clean_failed.append(filename)

    evil_bypassed = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(
            ["python3", sanitizer_path, filepath],
            capture_output=True
        )
        # Evil files should be rejected (exit code 1)
        if result.returncode == 0:
            evil_bypassed.append(filename)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    assert not errors, " | ".join(errors)