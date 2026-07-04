# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitize.sh"
EVIL_DIR = "/app/tests/evil"
CLEAN_DIR = "/app/tests/clean"

def get_expected_output(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        return ""

    expected_lines = [lines[0]] # Header
    for line in lines[1:]:
        if "_STALE_" not in line:
            expected_lines.append(line)

    return "".join(expected_lines)

def run_script_on_file(filepath):
    result = subprocess.run(
        ["bash", SCRIPT_PATH, filepath],
        capture_output=True,
        text=True
    )
    return result.stdout

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_clean_corpus():
    if not os.path.exists(CLEAN_DIR):
        pytest.skip(f"Clean corpus dir {CLEAN_DIR} not found")

    failed_files = []
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        expected = get_expected_output(filepath)
        actual = run_script_on_file(filepath)

        if actual.strip() != expected.strip():
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified or incorrectly processed: {', '.join(failed_files)}"

def test_evil_corpus():
    if not os.path.exists(EVIL_DIR):
        pytest.skip(f"Evil corpus dir {EVIL_DIR} not found")

    failed_files = []
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        expected = get_expected_output(filepath)
        actual = run_script_on_file(filepath)

        if actual.strip() != expected.strip():
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed or incorrectly processed: {', '.join(failed_files)}"