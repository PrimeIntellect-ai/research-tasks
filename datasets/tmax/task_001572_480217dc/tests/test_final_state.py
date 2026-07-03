# test_final_state.py

import os
import subprocess
import pytest

def test_sanitizer_executable_exists():
    executable_path = "/home/user/sanitizer"
    assert os.path.isfile(executable_path), f"Executable not found: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_clean_corpus_accepted():
    executable_path = "/home/user/sanitizer"
    clean_dir = "/app/clean"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "rb") as f:
            result = subprocess.run([executable_path], stdin=f, capture_output=True)
            if result.returncode != 0:
                failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected instead of accepted). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    executable_path = "/home/user/sanitizer"
    evil_dir = "/app/evil"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "rb") as f:
            result = subprocess.run([executable_path], stdin=f, capture_output=True)
            if result.returncode == 0:
                failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted instead of rejected). Offending files: {', '.join(failed_files)}")