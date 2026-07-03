# test_final_state.py
import os
import subprocess
import pytest

def test_loc_filter_executable_exists():
    executable_path = "/home/user/loc_filter"
    assert os.path.exists(executable_path), f"Executable not found at {executable_path}"
    assert os.path.isfile(executable_path), f"{executable_path} is not a file"
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable"

def test_clean_corpus():
    executable_path = "/home/user/loc_filter"
    clean_dir = "/app/corpus/clean/"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.jsonl')]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r') as f:
            result = subprocess.run([executable_path, "14.25"], stdin=f, capture_output=True, text=True)

        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected or crashed). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    executable_path = "/home/user/loc_filter"
    evil_dir = "/app/corpus/evil/"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.jsonl')]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r') as f:
            result = subprocess.run([executable_path, "14.25"], stdin=f, capture_output=True, text=True)

        if result.returncode != 1 or "REJECT" not in result.stdout:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted or wrong exit code). Offending files: {', '.join(failed_files)}")