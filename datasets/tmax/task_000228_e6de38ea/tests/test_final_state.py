# test_final_state.py
import os
import subprocess
import glob
import pytest

CLEAN_DIR = "/home/user/corpora/clean"
EVIL_DIR = "/home/user/corpora/evil"
SANITIZER = "/home/user/sanitizer"

def test_sanitizer_exists():
    assert os.path.exists(SANITIZER), f"Sanitizer executable not found at {SANITIZER}"
    assert os.access(SANITIZER, os.X_OK), f"Sanitizer at {SANITIZER} is not executable"

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    assert clean_files, f"No CSV files found in {CLEAN_DIR}"

    modified_files = []

    for file in clean_files:
        with open(file, 'rb') as f:
            input_data = f.read()

        result = subprocess.run([SANITIZER], input=input_data, capture_output=True)
        if result.returncode != 0:
            modified_files.append(os.path.basename(file) + " (crashed)")
            continue

        output_data = result.stdout

        input_lines = [line.strip() for line in input_data.split(b'\n') if line.strip()]
        output_lines = [line.strip() for line in output_data.split(b'\n') if line.strip()]

        if input_lines != output_lines:
            modified_files.append(os.path.basename(file))

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}"

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))
    assert evil_files, f"No CSV files found in {EVIL_DIR}"

    bypassed_files = []

    for file in evil_files:
        with open(file, 'rb') as f:
            input_data = f.read()

        result = subprocess.run([SANITIZER], input=input_data, capture_output=True)
        if result.returncode != 0:
            bypassed_files.append(os.path.basename(file) + " (crashed)")
            continue

        output_data = result.stdout

        input_lines = [line.strip() for line in input_data.split(b'\n') if line.strip()]
        output_lines = [line.strip() for line in output_data.split(b'\n') if line.strip()]

        # Expecting ONLY the header (1 line) or 0 lines if input was empty
        expected_len = 1 if input_lines else 0
        if len(output_lines) > expected_len:
            bypassed_files.append(os.path.basename(file))
        elif expected_len == 1 and output_lines[0] != input_lines[0]:
            bypassed_files.append(os.path.basename(file) + " (header modified)")

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"