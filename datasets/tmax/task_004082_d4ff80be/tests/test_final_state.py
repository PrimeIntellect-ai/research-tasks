# test_final_state.py
import os
import subprocess
import pytest

def test_filter_script_exists_and_executable():
    script_path = "/home/user/filter.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_clean_corpus_accepted():
    script_path = "/home/user/filter.sh"
    clean_corpus_path = "/truth/clean_corpus/"
    assert os.path.exists(clean_corpus_path), f"Directory {clean_corpus_path} does not exist."

    files = sorted([f for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))])
    assert len(files) > 0, "Clean corpus is empty."

    failed_files = []
    for f in files:
        file_path = os.path.join(clean_corpus_path, f)
        result = subprocess.run([script_path, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    script_path = "/home/user/filter.sh"
    evil_corpus_path = "/truth/evil_corpus/"
    assert os.path.exists(evil_corpus_path), f"Directory {evil_corpus_path} does not exist."

    files = sorted([f for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))])
    assert len(files) > 0, "Evil corpus is empty."

    bypassed_files = []
    for f in files:
        file_path = os.path.join(evil_corpus_path, f)
        result = subprocess.run([script_path, file_path], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(f)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(files)} evil bypassed (accepted or wrong exit code). Offending files: {', '.join(bypassed_files)}")