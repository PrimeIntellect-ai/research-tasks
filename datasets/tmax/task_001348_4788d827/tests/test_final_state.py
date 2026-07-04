# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitize.py"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_sanitizer_behavior():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    # Run on clean corpus
    result_clean = subprocess.run(["python3", SCRIPT_PATH, CLEAN_DIR], capture_output=True, text=True)
    assert result_clean.returncode == 0, f"Script failed on clean corpus:\n{result_clean.stderr}"

    clean_lines = [line.strip() for line in result_clean.stdout.strip().split("\n") if line.strip()]
    clean_results = {}
    for line in clean_lines:
        parts = line.split(":")
        if len(parts) >= 2:
            clean_results[parts[0].strip()] = parts[1].strip()

    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.cypher')]
    clean_modified = []
    for f in clean_files:
        if clean_results.get(f) != "ACCEPT":
            clean_modified.append(f)

    # Run on evil corpus
    result_evil = subprocess.run(["python3", SCRIPT_PATH, EVIL_DIR], capture_output=True, text=True)
    assert result_evil.returncode == 0, f"Script failed on evil corpus:\n{result_evil.stderr}"

    evil_lines = [line.strip() for line in result_evil.stdout.strip().split("\n") if line.strip()]
    evil_results = {}
    for line in evil_lines:
        parts = line.split(":")
        if len(parts) >= 2:
            evil_results[parts[0].strip()] = parts[1].strip()

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.cypher')]
    evil_bypassed = []
    for f in evil_files:
        if evil_results.get(f) != "REJECT":
            evil_bypassed.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))