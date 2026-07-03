# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/query_validator.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_script_exists():
    """Ensure the user created the query_validator.py script."""
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_clean_corpus():
    """Ensure all clean queries are accepted with exactly 'CLEAN' and exit code 0."""
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    failed_files = []

    for f in clean_files:
        path = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run(["python3", SCRIPT_PATH, path], capture_output=True, text=True)
        output = result.stdout.strip()

        if result.returncode != 0 or output != "CLEAN":
            failed_files.append((f, result.returncode, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean modified (rejected or failed). Offending files: "
        error_msg += ", ".join([f"{f} (code: {c}, out: {o})" for f, c, o in failed_files])
        pytest.fail(error_msg)

def test_evil_corpus():
    """Ensure all evil queries are rejected with exactly 'EVIL' and exit code 1."""
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    failed_files = []

    for f in evil_files:
        path = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run(["python3", SCRIPT_PATH, path], capture_output=True, text=True)
        output = result.stdout.strip()

        if result.returncode != 1 or output != "EVIL":
            failed_files.append((f, result.returncode, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted or failed incorrectly). Offending files: "
        error_msg += ", ".join([f"{f} (code: {c}, out: {o})" for f, c, o in failed_files])
        pytest.fail(error_msg)