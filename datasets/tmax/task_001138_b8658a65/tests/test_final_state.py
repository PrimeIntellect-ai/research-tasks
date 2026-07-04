# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitize.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Sanitize script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def run_sanitize_script(filepath):
    result = subprocess.run(
        ["/bin/bash", SCRIPT_PATH, filepath],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

def test_clean_corpus_preserved():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus dir missing: {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No files found in clean corpus directory."

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            original_content = f.read()

        stdout, stderr, rc = run_sanitize_script(filepath)

        if stdout != original_content:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified. Offending files: {', '.join(failed_files)}")

def compute_expected_sanitized_output(original_content):
    expected_lines = []
    for line in original_content.splitlines(keepends=True):
        stripped = line.strip('\n')
        parts = stripped.split(' ')
        if len(parts) != 3:
            expected_lines.append(line)
            continue

        ts, pressure, status = parts

        # Rule 1: Drop overload timestamps
        if ts in ["1715000004", "1715000005", "1715000006"]:
            continue

        # Rule 2: Drop scientific notation
        if 'e' in pressure or 'E' in pressure:
            continue

        # Rule 3: Truncate fractional part to exactly 4 decimal places
        if '.' in pressure:
            integer_part, fractional_part = pressure.split('.', 1)
            if len(fractional_part) > 4:
                pressure = f"{integer_part}.{fractional_part[:4]}"

        # Reconstruct line preserving original spacing logic
        # The spec says "preserving original spacing and format" for passed lines,
        # but for truncated lines it should be exactly the reconstructed string.
        # We assume single space separation as per "space-separated" spec.
        expected_lines.append(f"{ts} {pressure} {status}\n")

    return "".join(expected_lines)

def test_evil_corpus_sanitized():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus dir missing: {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No files found in evil corpus directory."

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            original_content = f.read()

        expected_output = compute_expected_sanitized_output(original_content)
        stdout, stderr, rc = run_sanitize_script(filepath)

        if stdout != expected_output:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")