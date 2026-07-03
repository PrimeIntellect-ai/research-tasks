# test_final_state.py

import os
import subprocess
import glob
import pytest

SANITIZER_PATH = "/home/user/sanitizer"
AGGREGATE_PATH = "/home/user/aggregate.sh"
CRON_PATH = "/home/user/pipeline.cron"

def test_sanitizer_executable():
    assert os.path.isfile(SANITIZER_PATH), f"Sanitizer script not found at {SANITIZER_PATH}"
    assert os.access(SANITIZER_PATH, os.X_OK), f"Sanitizer script at {SANITIZER_PATH} is not executable"

def test_sanitizer_clean_corpus():
    clean_files = glob.glob("/app/corpus/clean/*.csv")
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for fpath in clean_files:
        with open(fpath, "rb") as f:
            input_data = f.read()

        result = subprocess.run([SANITIZER_PATH], input=input_data, capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))
            continue

        input_lines = [line for line in input_data.decode('utf-8').splitlines() if line.strip()]
        output_lines = [line for line in result.stdout.decode('utf-8').splitlines() if line.strip()]

        if len(output_lines) != len(input_lines):
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified or rejected: {', '.join(failed_files)}"

def test_sanitizer_evil_corpus():
    evil_files = glob.glob("/app/corpus/evil/*.csv")
    assert evil_files, "No evil corpus files found."

    failed_files = []
    for fpath in evil_files:
        with open(fpath, "rb") as f:
            input_data = f.read()

        result = subprocess.run([SANITIZER_PATH], input=input_data, capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))
            continue

        output_lines = [line for line in result.stdout.decode('utf-8').splitlines() if line.strip()]
        # Output should be empty or just the header (1 line)
        if len(output_lines) > 1:
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {', '.join(failed_files)}"

def test_aggregate_script():
    assert os.path.isfile(AGGREGATE_PATH), f"Aggregate script not found at {AGGREGATE_PATH}"
    assert os.access(AGGREGATE_PATH, os.X_OK), f"Aggregate script at {AGGREGATE_PATH} is not executable"

    with open(AGGREGATE_PATH, "r") as f:
        content = f.read()

    # Check for 30-minute bucketing logic in some form
    assert "30" in content, "Aggregate script does not seem to implement 30-minute time bucketing."

def test_cron_file():
    assert os.path.isfile(CRON_PATH), f"Cron file not found at {CRON_PATH}"

    with open(CRON_PATH, "r") as f:
        content = f.read()

    assert "15" in content, "Cron file does not seem to schedule every 15 minutes."
    assert "aggregate.sh" in content, "Cron file does not reference aggregate.sh"
    assert "/tmp/latest.csv" in content, "Cron file does not reference /tmp/latest.csv"