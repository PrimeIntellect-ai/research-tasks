# test_final_state.py
import os
import sys
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/dataset_filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Target script {SCRIPT_PATH} does not exist."

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    assert len(clean_files) > 0, f"No files found in clean corpus {CLEAN_CORPUS_DIR}."

    failed_files = []

    for file_path in clean_files:
        if not os.path.isfile(file_path):
            continue

        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, file_path],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if result.returncode != 0 or output != "ACCEPT":
            failed_files.append((os.path.basename(file_path), result.returncode, output))

    if failed_files:
        details = ", ".join([f"{f} (code {c}, out '{o}')" for f, c, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {details}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    assert len(evil_files) > 0, f"No files found in evil corpus {EVIL_CORPUS_DIR}."

    failed_files = []

    for file_path in evil_files:
        if not os.path.isfile(file_path):
            continue

        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, file_path],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if result.returncode != 1 or output != "REJECT":
            failed_files.append((os.path.basename(file_path), result.returncode, output))

    if failed_files:
        details = ", ".join([f"{f} (code {c}, out '{o}')" for f, c, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed/accepted. Offending files: {details}")