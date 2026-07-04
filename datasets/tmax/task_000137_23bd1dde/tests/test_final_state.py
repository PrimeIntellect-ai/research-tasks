# test_final_state.py
import os
import subprocess
import pytest

def test_sanitizer_exists_and_executable():
    executable_path = "/home/user/audio_sanitizer"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"Executable {executable_path} is not executable."

def test_adversarial_corpus():
    executable_path = "/home/user/audio_sanitizer"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([executable_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([executable_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)