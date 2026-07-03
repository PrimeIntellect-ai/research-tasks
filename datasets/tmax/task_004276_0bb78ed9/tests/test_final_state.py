# test_final_state.py

import os
import subprocess
import pytest

def test_event_indices():
    indices_file = "/home/user/event_indices.txt"
    assert os.path.isfile(indices_file), f"Missing {indices_file}"

    with open(indices_file, "r") as f:
        content = f.read().strip().split()

    expected_indices = ["5", "12", "19", "34", "51"]
    assert content == expected_indices, f"Expected indices {expected_indices}, but got {content}"

def test_config_sanitizer_executable():
    executable = "/home/user/config_sanitizer"
    assert os.path.isfile(executable), f"Missing executable {executable}"
    assert os.access(executable, os.X_OK), f"{executable} is not executable"

def test_config_sanitizer_clean_corpus():
    executable = "/home/user/config_sanitizer"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Missing clean corpus dir {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([executable, filepath], capture_output=True, text=True)
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {failed_files}"

def test_config_sanitizer_evil_corpus():
    executable = "/home/user/config_sanitizer"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Missing evil corpus dir {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([executable, filepath], capture_output=True, text=True)
        if result.returncode != 1 or "REJECT" not in result.stdout:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failed_files}"