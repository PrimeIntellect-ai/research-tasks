# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/validate_configs.py"
EVIL_DIR = "/app/configs/evil/"
CLEAN_DIR = "/app/configs/clean/"

def run_script(directory):
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    result = subprocess.run(
        ["python3", SCRIPT_PATH, directory],
        capture_output=True,
        text=True
    )
    return result.stdout

def parse_output(output):
    results = {}
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
        if ": " in line:
            filename, status = line.split(": ", 1)
            results[filename.strip()] = status.strip()
    return results

def test_evil_corpus():
    stdout = run_script(EVIL_DIR)
    results = parse_output(stdout)

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    bypassed = []

    for f in evil_files:
        if results.get(f) != "INVALID":
            bypassed.append(f)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}"

def test_clean_corpus():
    stdout = run_script(CLEAN_DIR)
    results = parse_output(stdout)

    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]
    modified = []

    for f in clean_files:
        if results.get(f) != "VALID":
            modified.append(f)

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified/rejected: {modified}"