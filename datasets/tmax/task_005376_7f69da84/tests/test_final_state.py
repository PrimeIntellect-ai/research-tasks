# test_final_state.py
import os
import subprocess
import pytest

BINARY_PATH = "/home/user/pipeline_guard/target/release/pipeline_guard"
CLEAN_CORPUS = "/home/user/corpora/clean"
EVIL_CORPUS = "/home/user/corpora/evil"

def test_binary_exists_and_executable():
    assert os.path.exists(BINARY_PATH), f"Binary not found at {BINARY_PATH}"
    assert os.path.isfile(BINARY_PATH), f"{BINARY_PATH} is not a file"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_clean_corpus():
    assert os.path.exists(CLEAN_CORPUS), f"Clean corpus directory {CLEAN_CORPUS} not found"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "Clean corpus is empty"

    failed_files = []
    for f in clean_files:
        file_path = os.path.join(CLEAN_CORPUS, f)
        with open(file_path, 'rb') as fp:
            result = subprocess.run([BINARY_PATH], stdin=fp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.exists(EVIL_CORPUS), f"Evil corpus directory {EVIL_CORPUS} not found"
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "Evil corpus is empty"

    failed_files = []
    for f in evil_files:
        file_path = os.path.join(EVIL_CORPUS, f)
        with open(file_path, 'rb') as fp:
            result = subprocess.run([BINARY_PATH], stdin=fp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(failed_files)}")