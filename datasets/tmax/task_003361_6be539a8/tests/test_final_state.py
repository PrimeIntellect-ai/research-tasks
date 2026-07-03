# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_classifier_clean_corpus():
    script_path = "/home/user/profile_classifier.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    clean_dir = "/app/corpora/clean"
    clean_files = sorted(glob.glob(os.path.join(clean_dir, "*.csv")))
    assert len(clean_files) > 0, "No clean corpus files found in /app/corpora/clean"

    failed_files = []

    for file_path in clean_files:
        result = subprocess.run(
            ["python3", script_path, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected instead of accepted). Offending files: {', '.join(failed_files)}")

def test_classifier_evil_corpus():
    script_path = "/home/user/profile_classifier.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    evil_dir = "/app/corpora/evil"
    evil_files = sorted(glob.glob(os.path.join(evil_dir, "*.csv")))
    assert len(evil_files) > 0, "No evil corpus files found in /app/corpora/evil"

    failed_files = []

    for file_path in evil_files:
        result = subprocess.run(
            ["python3", script_path, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 1:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted instead of rejected). Offending files: {', '.join(failed_files)}")