# test_final_state.py

import os
import subprocess
import pytest

def test_build_validator_exists():
    script_path = "/home/user/build_validator.py"
    assert os.path.isfile(script_path), f"The required script {script_path} does not exist."

def test_corpus_validation():
    script_path = "/home/user/build_validator.py"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_subdirs = [os.path.join(clean_dir, d) for d in os.listdir(clean_dir) if os.path.isdir(os.path.join(clean_dir, d))]
    evil_subdirs = [os.path.join(evil_dir, d) for d in os.listdir(evil_dir) if os.path.isdir(os.path.join(evil_dir, d))]

    failed_clean = []
    for d in clean_subdirs:
        result = subprocess.run(["python3", script_path, d], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(d))

    failed_evil = []
    for d in evil_subdirs:
        result = subprocess.run(["python3", script_path, d], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(d))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_subdirs)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_subdirs)} evil bypassed: {', '.join(failed_evil)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))