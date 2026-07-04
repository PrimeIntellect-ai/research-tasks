# test_final_state.py

import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/query_filter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.R_OK), f"The script {SCRIPT_PATH} is not readable."

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.sql"))
    assert len(clean_files) > 0, f"No clean SQL files found in {CLEAN_CORPUS_DIR}"

    rejected_files = []

    for sql_file in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, sql_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "ACCEPT":
            rejected_files.append((os.path.basename(sql_file), output, result.stderr.strip()))

    if rejected_files:
        details = "\n".join([f"{f}: expected ACCEPT, got {out!r} (stderr: {err!r})" for f, out, err in rejected_files])
        pytest.fail(f"{len(rejected_files)} of {len(clean_files)} clean queries were REJECTED or failed:\n{details}")

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.sql"))
    assert len(evil_files) > 0, f"No evil SQL files found in {EVIL_CORPUS_DIR}"

    accepted_files = []

    for sql_file in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, sql_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "REJECT":
            accepted_files.append((os.path.basename(sql_file), output, result.stderr.strip()))

    if accepted_files:
        details = "\n".join([f"{f}: expected REJECT, got {out!r} (stderr: {err!r})" for f, out, err in accepted_files])
        pytest.fail(f"{len(accepted_files)} of {len(evil_files)} evil queries bypassed the filter:\n{details}")