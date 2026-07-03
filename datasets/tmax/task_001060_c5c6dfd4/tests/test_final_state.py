# test_final_state.py

import os
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_filter_script_exists_and_executable():
    assert os.path.exists(FILTER_SCRIPT), f"{FILTER_SCRIPT} does not exist."
    assert os.path.isfile(FILTER_SCRIPT), f"{FILTER_SCRIPT} is not a file."
    assert os.access(FILTER_SCRIPT, os.X_OK), f"{FILTER_SCRIPT} is not executable."

def test_filter_adversarial_corpus():
    if not os.path.exists(FILTER_SCRIPT) or not os.access(FILTER_SCRIPT, os.X_OK):
        pytest.fail(f"Cannot test corpus: {FILTER_SCRIPT} missing or not executable.")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_modified = []
    evil_bypassed = []

    # Test clean corpus
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'rb') as f:
            input_data = f.read()

        result = subprocess.run([FILTER_SCRIPT], input=input_data, capture_output=True)

        # We expect the clean rows to be preserved. 
        # Compare non-empty lines to avoid newline issues.
        input_lines = [line.strip() for line in input_data.decode('utf-8', errors='replace').splitlines() if line.strip()]
        output_lines = [line.strip() for line in result.stdout.decode('utf-8', errors='replace').splitlines() if line.strip()]

        if input_lines != output_lines:
            clean_modified.append(filename)

    # Test evil corpus
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'rb') as f:
            input_data = f.read()

        result = subprocess.run([FILTER_SCRIPT], input=input_data, capture_output=True)

        output_lines = [line.strip() for line in result.stdout.decode('utf-8', errors='replace').splitlines() if line.strip()]

        if len(output_lines) > 0:
            evil_bypassed.append(filename)

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_etl_script_exists_and_executable():
    etl_script = "/home/user/etl.sh"
    assert os.path.exists(etl_script), f"{etl_script} does not exist."
    assert os.path.isfile(etl_script), f"{etl_script} is not a file."
    assert os.access(etl_script, os.X_OK), f"{etl_script} is not executable."