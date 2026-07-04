# test_final_state.py

import os
import subprocess
import csv
import pytest

BINARY_PATH = "/home/user/log_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def get_expected_output(csv_path):
    expected_lines = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 5:
                continue
            event_id, timestamp, cpu, mem, retry = row
            expected_lines.append(f"{event_id},{timestamp},CPU_Usage,{cpu}")
            expected_lines.append(f"{event_id},{timestamp},Memory_Usage,{mem}")
    return expected_lines

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    assert clean_files, "No clean CSV files found in corpus"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True)

        if result.returncode != 0:
            failed_files.append((filename, f"Exit code {result.returncode} instead of 0"))
            continue

        expected_lines = get_expected_output(filepath)
        actual_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # OpenMP might change the order of output
        if sorted(expected_lines) != sorted(actual_lines):
            failed_files.append((filename, "Output data does not match expected long format"))

    if failed_files:
        errors = "\n".join(f"{f}: {err}" for f, err in failed_files)
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files failed:\n{errors}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    assert evil_files, "No evil CSV files found in corpus"

    bypassed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True)

        if result.returncode == 0:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed validation:\n" + "\n".join(bypassed_files))