# test_final_state.py

import os
import subprocess
import pytest

def run_filter(file_path):
    result = subprocess.run(
        ["python3", "/home/user/security_filter.py", file_path],
        capture_output=True,
        text=True
    )
    return result.returncode

def test_security_filter_clean_corpus():
    clean_dir = "/app/eval_corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        code = run_filter(path)
        if code != 0:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {failed_files}"

def test_security_filter_evil_corpus():
    evil_dir = "/app/eval_corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        code = run_filter(path)
        if code != 1:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {failed_files}"

def test_make_check_fails():
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), "Makefile not found at /home/user/Makefile"

    result = subprocess.run(
        ["make", "check"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert result.returncode != 0, "make check should fail (non-zero exit code) because the screenshot contains leaked info."

def test_hypothesis_script_runs():
    test_script = "/home/user/test_filter.py"
    assert os.path.isfile(test_script), f"Test script not found at {test_script}"

    result = subprocess.run(
        ["python3", test_script],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"test_filter.py failed to run successfully.\nStdout: {result.stdout}\nStderr: {result.stderr}"