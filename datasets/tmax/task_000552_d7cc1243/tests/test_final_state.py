# test_final_state.py
import os
import glob
import subprocess
import pytest

BINARY_PATH = "/home/user/workspace/sanitizer"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Binary not found at {BINARY_PATH}. Did you compile it?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert clean_files, f"No clean corpus files found in {CLEAN_CORPUS_DIR}"
    assert evil_files, f"No evil corpus files found in {EVIL_CORPUS_DIR}"

    clean_modified = []
    evil_bypassed = []

    for c_file in clean_files:
        with open(c_file, 'r') as f:
            input_data = f.read()

        result = subprocess.run(
            [BINARY_PATH],
            input=input_data,
            text=True,
            capture_output=True
        )

        input_count = len([line for line in input_data.splitlines() if line.strip()])
        output_count = len([line for line in result.stdout.splitlines() if line.strip()])

        # Clean corpus: 100% preserved
        if input_count != output_count:
            clean_modified.append(os.path.basename(c_file))

    for e_file in evil_files:
        with open(e_file, 'r') as f:
            input_data = f.read()

        result = subprocess.run(
            [BINARY_PATH],
            input=input_data,
            text=True,
            capture_output=True
        )

        output_count = len([line for line in result.stdout.splitlines() if line.strip()])

        # Evil corpus: 100% rejected (only the header should remain -> exactly 1 line)
        if output_count != 1:
            evil_bypassed.append(os.path.basename(e_file))

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))