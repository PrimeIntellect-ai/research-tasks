# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/token_filter.py"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def run_script_and_parse_output(directory):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, directory],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"

    accepts = set()
    rejects = set()

    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("ACCEPT: "):
            accepts.add(line[len("ACCEPT: "):].strip())
        elif line.startswith("REJECT: "):
            rejects.add(line[len("REJECT: "):].strip())

    return accepts, rejects

def test_clean_corpus():
    clean_files = set(os.listdir(CLEAN_DIR))
    assert len(clean_files) > 0, "Clean corpus is empty."

    accepts, rejects = run_script_and_parse_output(CLEAN_DIR)

    rejected_clean = clean_files.intersection(rejects)
    missing_clean = clean_files - accepts

    errors = []
    if rejected_clean:
        errors.append(f"{len(rejected_clean)} of {len(clean_files)} clean files were incorrectly rejected: {', '.join(rejected_clean)}")
    if missing_clean and not rejected_clean:
        errors.append(f"{len(missing_clean)} clean files were not accepted: {', '.join(missing_clean)}")

    assert not errors, "\n".join(errors)

def test_evil_corpus():
    evil_files = set(os.listdir(EVIL_DIR))
    assert len(evil_files) > 0, "Evil corpus is empty."

    accepts, rejects = run_script_and_parse_output(EVIL_DIR)

    accepted_evil = evil_files.intersection(accepts)
    missing_evil = evil_files - rejects

    errors = []
    if accepted_evil:
        errors.append(f"{len(accepted_evil)} of {len(evil_files)} evil files bypassed the filter and were accepted: {', '.join(accepted_evil)}")
    if missing_evil and not accepted_evil:
        errors.append(f"{len(missing_evil)} evil files were not rejected: {', '.join(missing_evil)}")

    assert not errors, "\n".join(errors)