# test_final_state.py
import os
import subprocess
import shutil
import pytest

SCRIPT_PATH = "/home/user/etl_filter.sh"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_etl_filter_clean_corpus():
    out_dir = "/tmp/test_clean_out"
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    result = subprocess.run([SCRIPT_PATH, CLEAN_CORPUS, out_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on clean corpus with error: {result.stderr}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.csv')]
    out_files = set(os.listdir(out_dir))

    missing_clean = []
    for f in clean_files:
        if f not in out_files:
            missing_clean.append(f)

    if missing_clean:
        pytest.fail(f"{len(missing_clean)} of {len(clean_files)} clean modified (not preserved). Missing files: {', '.join(missing_clean)}")

def test_etl_filter_evil_corpus():
    out_dir = "/tmp/test_evil_out"
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    result = subprocess.run([SCRIPT_PATH, EVIL_CORPUS, out_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on evil corpus with error: {result.stderr}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.csv')]
    out_files = set(os.listdir(out_dir))

    bypassed_evil = []
    for f in evil_files:
        if f in out_files:
            bypassed_evil.append(f)

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed (not rejected). Offending files: {', '.join(bypassed_evil)}")