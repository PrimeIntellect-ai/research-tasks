# test_final_state.py

import os
import subprocess
import pytest

def test_leak_analysis_content():
    path = "/home/user/leak_analysis.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    expected = "BAZINGA:9F8E7D6C5B4A3928"
    assert content == expected, f"Expected content '{expected}', but got '{content}'"

def test_detector_executable():
    path = "/home/user/detector"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile detector.cpp?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_adversarial_corpus():
    detector = "/home/user/detector"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) == 50, f"Expected 50 clean files, found {len(clean_files)}."
    assert len(evil_files) == 50, f"Expected 50 evil files, found {len(evil_files)}."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([detector, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([detector, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))