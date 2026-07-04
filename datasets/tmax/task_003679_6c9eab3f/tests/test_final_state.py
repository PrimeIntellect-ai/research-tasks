# test_final_state.py

import os
import subprocess
import pytest

def test_log_proc_built():
    log_proc_path = "/app/vendored/log-processor-2.0/log-proc"
    assert os.path.isfile(log_proc_path), f"Expected compiled binary at {log_proc_path}"
    assert os.access(log_proc_path, os.X_OK), f"Expected {log_proc_path} to be executable"

def test_classifier_built():
    classifier_path = "/home/user/classifier"
    assert os.path.isfile(classifier_path), f"Expected compiled classifier at {classifier_path}"
    assert os.access(classifier_path, os.X_OK), f"Expected {classifier_path} to be executable"

def test_classifier_clean_corpus():
    classifier_path = "/home/user/classifier"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    failed_files = []
    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        result = subprocess.run([classifier_path, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {failed_files}")

def test_classifier_evil_corpus():
    classifier_path = "/home/user/classifier"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(evil_dir), f"Directory {evil_dir} does not exist"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    failed_files = []
    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        result = subprocess.run([classifier_path, file_path], capture_output=True)
        if result.returncode != 1:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {failed_files}")