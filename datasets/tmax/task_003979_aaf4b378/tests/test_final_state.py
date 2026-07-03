# test_final_state.py
import os
import stat
import subprocess
import pytest

FILTER_BIN = "/home/user/filter_bin"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_filter_bin_exists_and_permissions():
    assert os.path.isfile(FILTER_BIN), f"The binary {FILTER_BIN} does not exist."

    st = os.stat(FILTER_BIN)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o755, f"Permissions of {FILTER_BIN} are {oct(permissions)}, expected 0o755."

def test_evil_corpus_rejected():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus directory {EVIL_CORPUS_DIR} is missing."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in {EVIL_CORPUS_DIR}."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil payloads bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")

def test_clean_corpus_preserved():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus directory {CLEAN_CORPUS_DIR} is missing."

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in {CLEAN_CORPUS_DIR}."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([FILTER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean payloads modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")