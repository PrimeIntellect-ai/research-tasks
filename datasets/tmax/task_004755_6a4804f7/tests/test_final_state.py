# test_final_state.py

import os
import subprocess
import glob
import stat
import pytest

ENTRY_POINT = "/home/user/run_detector.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_entry_point_exists_and_executable():
    assert os.path.isfile(ENTRY_POINT), f"Entry point script {ENTRY_POINT} does not exist."
    st = os.stat(ENTRY_POINT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Entry point script {ENTRY_POINT} is not executable."

def test_corpora_classification():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    clean_rejected = []
    for fpath in clean_files:
        result = subprocess.run([ENTRY_POINT, fpath], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(fpath))

    evil_bypassed = []
    for fpath in evil_files:
        result = subprocess.run([ENTRY_POINT, fpath], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(fpath))

    errors = []
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_libtrajectory_so_exists():
    assert os.path.isfile("/home/user/libtrajectory/libtrajectory.so"), "libtrajectory.so was not built."