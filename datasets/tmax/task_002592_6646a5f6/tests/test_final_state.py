# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_corrupted_frame_txt():
    path = "/home/user/corrupted_frame.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "74", f"Expected corrupted_frame.txt to contain '74', but found '{content}'"

def test_sanitizer_exists():
    path = "/home/user/sanitizer.py"
    assert os.path.isfile(path), f"Missing required script: {path}"

def test_sanitizer_evil_corpus():
    sanitizer_script = "/home/user/sanitizer.py"
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.mp4"))

    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", sanitizer_script, filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(
            f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the sanitizer (expected exit code 1). "
            f"Offending files: {', '.join(bypassed_files)}"
        )

def test_sanitizer_clean_corpus():
    sanitizer_script = "/home/user/sanitizer.py"
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.mp4"))

    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    modified_files = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", sanitizer_script, filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        pytest.fail(
            f"{len(modified_files)} of {len(clean_files)} clean files were incorrectly rejected (expected exit code 0). "
            f"Offending files: {', '.join(modified_files)}"
        )