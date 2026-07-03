# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect_slip.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.ibk.gz"))
    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"

    failed_files = []

    for file_path in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or "SAFE" not in result.stdout.strip():
            failed_files.append(os.path.basename(file_path))

    assert not failed_files, (
        f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly flagged as MALICIOUS or failed. "
        f"Offending files: {', '.join(failed_files)}"
    )

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.ibk.gz"))
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    failed_files = []

    for file_path in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 1 or "MALICIOUS" not in result.stdout.strip():
            failed_files.append(os.path.basename(file_path))

    assert not failed_files, (
        f"{len(failed_files)} of {len(evil_files)} evil files bypassed detection. "
        f"Offending files: {', '.join(failed_files)}"
    )