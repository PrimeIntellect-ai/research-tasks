# test_final_state.py

import os
import subprocess
import glob
import pytest

AGENT_BIN = "/home/user/classifier"
CLEAN_DIR = "/verify/corpus/clean"
EVIL_DIR = "/verify/corpus/evil"

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_BIN), f"The agent binary is missing at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"The agent binary at {AGENT_BIN} is not executable"

def test_classifier_clean_corpus():
    clean_files = sorted(glob.glob(os.path.join(CLEAN_DIR, "*.csv")))
    assert len(clean_files) > 0, f"No clean CSV files found in {CLEAN_DIR}"

    failed_files = []

    for csv_file in clean_files:
        result = subprocess.run(
            [AGENT_BIN, csv_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected (should be CLEAN, exit 0). Offending files: {', '.join(failed_files)}")

def test_classifier_evil_corpus():
    evil_files = sorted(glob.glob(os.path.join(EVIL_DIR, "*.csv")))
    assert len(evil_files) > 0, f"No evil CSV files found in {EVIL_DIR}"

    failed_files = []

    for csv_file in evil_files:
        result = subprocess.run(
            [AGENT_BIN, csv_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if result.returncode != 1 or output != "EVIL":
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be EVIL, exit 1). Offending files: {', '.join(failed_files)}")