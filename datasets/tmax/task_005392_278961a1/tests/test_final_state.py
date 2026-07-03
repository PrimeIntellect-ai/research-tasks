# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/query_filter.py"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def run_script(directory):
    result = subprocess.run(["python3", SCRIPT_PATH, directory], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"
    lines = result.stdout.strip().split('\n')

    parsed_results = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.rsplit(',', 1)
        if len(parts) == 2:
            filename = os.path.basename(parts[0].strip())
            status = parts[1].strip()
            parsed_results[filename] = status

    return parsed_results

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Missing script: {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path is not a file: {SCRIPT_PATH}"

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in {CLEAN_DIR}"

    results = run_script(CLEAN_DIR)

    rejected_files = []
    missing_files = []

    for f in clean_files:
        if f not in results:
            missing_files.append(f)
        elif results[f] != "ACCEPT":
            rejected_files.append(f)

    error_msg = []
    if rejected_files:
        error_msg.append(f"{len(rejected_files)} of {len(clean_files)} clean queries modified/rejected: {', '.join(rejected_files)}")
    if missing_files:
        error_msg.append(f"{len(missing_files)} clean queries missing from output: {', '.join(missing_files)}")

    assert not error_msg, " | ".join(error_msg)

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in {EVIL_DIR}"

    results = run_script(EVIL_DIR)

    accepted_files = []
    missing_files = []

    for f in evil_files:
        if f not in results:
            missing_files.append(f)
        elif results[f] != "REJECT":
            accepted_files.append(f)

    error_msg = []
    if accepted_files:
        error_msg.append(f"{len(accepted_files)} of {len(evil_files)} evil queries bypassed/accepted: {', '.join(accepted_files)}")
    if missing_files:
        error_msg.append(f"{len(missing_files)} evil queries missing from output: {', '.join(missing_files)}")

    assert not error_msg, " | ".join(error_msg)