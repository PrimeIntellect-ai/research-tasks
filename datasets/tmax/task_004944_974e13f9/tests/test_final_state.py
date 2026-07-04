# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_makefile_fixed():
    makefile_path = "/app/cJSON-1.7.15/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "broken-gcc" not in content, "The Makefile still contains 'broken-gcc'."

def test_binary_exists_and_executable():
    binary_path = "/home/user/filter_pipelines"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable."

def test_adversarial_corpus():
    binary_path = "/home/user/filter_pipelines"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_modified = []
    evil_bypassed = []

    for clean_file in clean_files:
        with open(clean_file, "rb") as f:
            input_data = f.read()

        result = subprocess.run([binary_path], input=input_data, capture_output=True)
        if result.stdout != input_data:
            clean_modified.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        with open(evil_file, "rb") as f:
            input_data = f.read()

        result = subprocess.run([binary_path], input=input_data, capture_output=True)
        if result.stdout.strip() != b"":
            evil_bypassed.append(os.path.basename(evil_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))