# test_final_state.py

import os
import re
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/process_pipeline.sh"
CLEAN_CORPUS_DIR = "/home/user/corpora/clean"
EVIL_CORPUS_DIR = "/home/user/corpora/evil"

def get_expected_clean_output(input_filepath):
    expected_lines = []
    with open(input_filepath, 'r') as f:
        for line in f:
            if "DEBUG_TRACE" in line:
                continue
            # Mask SSNs
            masked_line = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', line)
            expected_lines.append(masked_line)
    return "".join(expected_lines)

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_evil_corpus_rejected():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_CORPUS_DIR} not found.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    bypassed_files = []

    for filename in evil_files:
        input_file = os.path.join(EVIL_CORPUS_DIR, filename)
        with tempfile.NamedTemporaryFile() as tmp_out:
            result = subprocess.run(
                [SCRIPT_PATH, input_file, tmp_out.name],
                capture_output=True
            )
            if result.returncode != 1:
                bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_clean_corpus_accepted():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_CORPUS_DIR} not found.")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    modified_files = []

    for filename in clean_files:
        input_file = os.path.join(CLEAN_CORPUS_DIR, filename)
        expected_output = get_expected_clean_output(input_file)

        with tempfile.NamedTemporaryFile() as tmp_out:
            result = subprocess.run(
                [SCRIPT_PATH, input_file, tmp_out.name],
                capture_output=True
            )

            if result.returncode != 0:
                modified_files.append(f"{filename} (exit code {result.returncode})")
                continue

            with open(tmp_out.name, 'r') as f:
                actual_output = f.read()

            if actual_output != expected_output:
                modified_files.append(f"{filename} (content mismatch)")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified or failed. Offending files: {', '.join(modified_files)}")