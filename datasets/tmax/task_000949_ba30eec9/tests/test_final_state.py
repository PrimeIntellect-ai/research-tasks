# test_final_state.py

import os
import subprocess
import pytest

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"
FILTER_BIN = "/home/user/filter"
PIPELINE_SCRIPT = "/home/user/pipeline.sh"

def test_filter_binary_exists():
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} does not exist. Did you compile your Go code?"
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable."

def test_pipeline_script_exists():
    assert os.path.isfile(PIPELINE_SCRIPT), f"{PIPELINE_SCRIPT} does not exist."
    assert os.access(PIPELINE_SCRIPT, os.X_OK), f"{PIPELINE_SCRIPT} is not executable."

def test_clean_corpus():
    if not os.path.isdir(CLEAN_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_DIR} not found.")

    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    modified = []

    for cf in clean_files:
        path = os.path.join(CLEAN_DIR, cf)
        with open(path, 'rb') as f:
            input_data = f.read()

        try:
            result = subprocess.run([FILTER_BIN], input=input_data, capture_output=True, timeout=5)
            # Compare lines to avoid minor trailing newline differences
            input_lines = [line.strip() for line in input_data.decode('utf-8').splitlines() if line.strip()]
            output_lines = [line.strip() for line in result.stdout.decode('utf-8').splitlines() if line.strip()]

            if input_lines != output_lines:
                modified.append(cf)
        except Exception:
            modified.append(cf)

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified: {modified}"

def test_evil_corpus():
    if not os.path.isdir(EVIL_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_DIR} not found.")

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    bypassed = []

    for ef in evil_files:
        path = os.path.join(EVIL_DIR, ef)
        with open(path, 'rb') as f:
            input_data = f.read()

        try:
            result = subprocess.run([FILTER_BIN], input=input_data, capture_output=True, timeout=5)
            output_lines = [line.strip() for line in result.stdout.decode('utf-8').splitlines() if line.strip()]

            if output_lines:
                bypassed.append(ef)
        except Exception:
            # If it crashes on evil input, it didn't strictly bypass, but it's not robust. 
            # We'll consider it a bypass of the proper filtering mechanism.
            bypassed.append(ef)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}"