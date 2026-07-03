# test_final_state.py

import os
import subprocess
import pytest

def test_red_frame_count():
    count_file = "/home/user/red_frame_count.txt"
    assert os.path.isfile(count_file), f"Missing red frame count file: {count_file}"
    with open(count_file, "r") as f:
        content = f.read().strip()
    assert content == "47", f"Expected red frame count to be '47', but got '{content}'"

def test_validator_executable_exists():
    executable = "/home/user/validator"
    assert os.path.isfile(executable), f"Missing validator executable: {executable}"
    assert os.access(executable, os.X_OK), f"Validator executable is not executable: {executable}"

def test_validator_clean_corpus():
    executable = "/home/user/validator"
    clean_dir = "/app/corpus/clean/"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    failed_clean = []
    for filepath in clean_files:
        result = subprocess.run([executable, filepath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(filepath))

    assert len(failed_clean) == 0, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}"

def test_validator_evil_corpus():
    executable = "/home/user/validator"
    evil_dir = "/app/corpus/evil/"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    bypassed_evil = []
    for filepath in evil_files:
        result = subprocess.run([executable, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(os.path.basename(filepath))

    assert len(bypassed_evil) == 0, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}"