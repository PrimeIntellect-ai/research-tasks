# test_final_state.py

import os
import re
import subprocess
import pytest

EXPECTED_HASH = "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
HASH_FILE = "/home/user/archive_hash.txt"
SCRIPT_FILE = "/home/user/filter_logs.sh"
CLEAN_CORPUS_DIR = "/app/verifier/corpus/clean"
EVIL_CORPUS_DIR = "/app/verifier/corpus/evil"

MALICIOUS_STRINGS = [
    "<script>",
    "javascript:",
    "onerror=",
    "' or 1=1",
    "union select"
]

def test_archive_hash_file():
    """Verify that the hash file exists and contains the correct SHA-256 hash."""
    assert os.path.isfile(HASH_FILE), f"Missing required hash file: {HASH_FILE}"

    with open(HASH_FILE, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_HASH, f"Hash file content is incorrect. Expected {EXPECTED_HASH}, got {content}"

def test_script_exists_and_executable():
    """Verify that the filter script exists and is executable."""
    assert os.path.isfile(SCRIPT_FILE), f"Missing required script file: {SCRIPT_FILE}"
    assert os.access(SCRIPT_FILE, os.X_OK), f"Script file is not executable: {SCRIPT_FILE}"

def process_line_python(line):
    """Python implementation of the expected filtering logic to generate truth data."""
    lower_line = line.lower()
    for bad in MALICIOUS_STRINGS:
        if bad in lower_line:
            return None  # Drop the line entirely

    # Redact SSNs
    redacted_line = re.sub(r'\d{3}-\d{2}-\d{4}', 'XXX-XX-XXXX', line)
    return redacted_line

def get_expected_output(filepath):
    """Generate the expected output for a given file."""
    expected_lines = []
    with open(filepath, "r") as f:
        for line in f:
            processed = process_line_python(line)
            if processed is not None:
                expected_lines.append(processed)
    return "".join(expected_lines)

def test_clean_corpus():
    """Verify that the script leaves clean files completely unmodified."""
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory not found: {CLEAN_CORPUS_DIR}")

    files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    if not files:
        pytest.skip("No files found in clean corpus.")

    modified_files = []

    for filename in files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)

        with open(filepath, "r") as f:
            expected_output = f.read()

        result = subprocess.run([SCRIPT_FILE, filepath], capture_output=True, text=True)

        if result.returncode != 0 or result.stdout != expected_output:
            modified_files.append(filename)

    assert not modified_files, f"{len(modified_files)} of {len(files)} clean modified. Offending files: {', '.join(modified_files)}"

def test_evil_corpus():
    """Verify that the script drops malicious lines and redacts SSNs in the evil corpus."""
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory not found: {EVIL_CORPUS_DIR}")

    files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    if not files:
        pytest.skip("No files found in evil corpus.")

    bypassed_files = []

    for filename in files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        expected_output = get_expected_output(filepath)

        result = subprocess.run([SCRIPT_FILE, filepath], capture_output=True, text=True)

        if result.returncode != 0 or result.stdout != expected_output:
            bypassed_files.append(filename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(files)} evil bypassed. Offending files: {', '.join(bypassed_files)}"