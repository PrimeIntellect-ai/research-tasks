# test_final_state.py
import os
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = "/app/sqlite-amalgamation/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "sqlite2.c" not in content, "The typo 'sqlite2.c' is still present in the Makefile."
    assert "sqlite3.c" in content, "The Makefile does not reference 'sqlite3.c' for compilation."

def test_backup_validator_binary_exists():
    binary_path = "/home/user/backup_validator"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing. Did you compile the C program?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_corpora_classification():
    binary_path = "/home/user/backup_validator"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"Directory {clean_dir} is missing."
    assert os.path.isdir(evil_dir), f"Directory {evil_dir} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.db')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.db')]

    assert len(clean_files) > 0, "No clean databases found in the corpus."
    assert len(evil_files) > 0, "No evil databases found in the corpus."

    clean_failures = []
    for db in clean_files:
        result = subprocess.run([binary_path, db], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            clean_failures.append(os.path.basename(db))

    evil_failures = []
    for db in evil_files:
        result = subprocess.run([binary_path, db], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            evil_failures.append(os.path.basename(db))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/failed: " + ", ".join(clean_failures))
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/failed: " + ", ".join(evil_failures))

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))