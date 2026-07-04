# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import pytest

SCRIPT_PATH = "/home/user/secure_extract.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
PASSWORD = "42"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_adversarial_corpus():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus missing at {CLEAN_CORPUS_DIR}"
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus missing at {EVIL_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    failed_clean = []
    failed_evil = []

    # Test clean corpus
    for clean_file in clean_files:
        dest_dir = tempfile.mkdtemp()
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, clean_file, dest_dir, PASSWORD],
                capture_output=True,
                text=True
            )
            if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
                failed_clean.append((os.path.basename(clean_file), result.returncode, result.stdout.strip()))
        finally:
            shutil.rmtree(dest_dir)

    # Test evil corpus
    for evil_file in evil_files:
        dest_dir = tempfile.mkdtemp()
        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, evil_file, dest_dir, PASSWORD],
                capture_output=True,
                text=True
            )
            if result.returncode != 1 or result.stdout.strip() != "REJECT":
                failed_evil.append((os.path.basename(evil_file), result.returncode, result.stdout.strip()))
        finally:
            shutil.rmtree(dest_dir)

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean archives rejected or failed:")
        for f, rc, out in failed_clean:
            error_messages.append(f"  - {f} (exit code: {rc}, stdout: '{out}')")

    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil archives bypassed or failed to reject properly:")
        for f, rc, out in failed_evil:
            error_messages.append(f"  - {f} (exit code: {rc}, stdout: '{out}')")

    assert not failed_clean and not failed_evil, "\n".join(error_messages)