# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validator.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_validator_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Validator script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_clean_corpus_accepted():
    assert os.path.exists(CLEAN_CORPUS_DIR), f"Clean corpus missing at {CLEAN_CORPUS_DIR}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert clean_files, "No files found in clean corpus directory."

    failed_files = []

    for token_file in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, token_file],
            capture_output=True,
            text=True
        )

        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "VALID":
            failed_files.append((os.path.basename(token_file), result.returncode, stdout))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean tokens rejected/modified.\n"
        for fname, rc, out in failed_files[:10]:
            error_msg += f"  - {fname}: exit code {rc}, stdout '{out}'\n"
        if len(failed_files) > 10:
            error_msg += f"  ... and {len(failed_files) - 10} more."
        pytest.fail(error_msg)

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR), f"Evil corpus missing at {EVIL_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert evil_files, "No files found in evil corpus directory."

    failed_files = []

    for token_file in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, token_file],
            capture_output=True,
            text=True
        )

        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "INVALID":
            failed_files.append((os.path.basename(token_file), result.returncode, stdout))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil tokens bypassed.\n"
        for fname, rc, out in failed_files[:10]:
            error_msg += f"  - {fname}: exit code {rc}, stdout '{out}'\n"
        if len(failed_files) > 10:
            error_msg += f"  ... and {len(failed_files) - 10} more."
        pytest.fail(error_msg)