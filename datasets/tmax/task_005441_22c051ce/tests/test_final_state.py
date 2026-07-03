# test_final_state.py

import os
import subprocess
import pytest

def test_sanitiser_exists_and_executable():
    sanitiser_path = "/home/user/sanitiser"
    assert os.path.isfile(sanitiser_path), f"Sanitiser executable not found at {sanitiser_path}"
    assert os.access(sanitiser_path, os.X_OK), f"Sanitiser at {sanitiser_path} is not executable"

def test_sanitiser_clean_corpus():
    sanitiser_path = "/home/user/sanitiser"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} not found"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []

    for file_path in clean_files:
        with open(file_path, 'rb') as f:
            content = f.read()

        result = subprocess.run([sanitiser_path], input=content, capture_output=True)

        if result.stdout != content:
            failed_files.append(os.path.basename(file_path))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified: {', '.join(failed_files)}"

def test_sanitiser_evil_corpus():
    sanitiser_path = "/home/user/sanitiser"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} not found"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_files = []

    for file_path in evil_files:
        with open(file_path, 'rb') as f:
            content = f.read()

        result = subprocess.run([sanitiser_path], input=content, capture_output=True)

        if result.stdout != b"":
            failed_files.append(os.path.basename(file_path))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"