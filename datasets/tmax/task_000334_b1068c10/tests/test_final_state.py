# test_final_state.py
import os
import sys
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitiser.py"
EVIL_DIR = "/app/evil_configs"
CLEAN_DIR = "/app/clean_configs"

def run_sanitiser(target_dir):
    """Helper to run the student's script and parse its JSON output."""
    assert os.path.isfile(SCRIPT_PATH), f"Sanitiser script not found at {SCRIPT_PATH}"

    result = subprocess.run(
        [sys.executable, SCRIPT_PATH, target_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on {target_dir} with return code {result.returncode}.\nStderr: {result.stderr}"

    try:
        output_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Script output is not valid JSON. Stdout: {result.stdout}")

    return output_json

def test_evil_corpus_rejected():
    """Verify that all files in the evil corpus are REJECTED."""
    assert os.path.isdir(EVIL_DIR), f"Evil corpus directory missing: {EVIL_DIR}"

    output = run_sanitiser(EVIL_DIR)
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.conf')]
    assert len(evil_files) > 0, f"No .conf files found in {EVIL_DIR}"

    bypassed = []
    for filename in evil_files:
        status = output.get(filename)
        if status != "REJECTED":
            bypassed.append(f"{filename} (status: {status})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil configs bypassed rejection:\n" + "\n".join(bypassed))

def test_clean_corpus_accepted():
    """Verify that all files in the clean corpus are ACCEPTED."""
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus directory missing: {CLEAN_DIR}"

    output = run_sanitiser(CLEAN_DIR)
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.conf')]
    assert len(clean_files) > 0, f"No .conf files found in {CLEAN_DIR}"

    rejected = []
    for filename in clean_files:
        status = output.get(filename)
        if status != "ACCEPTED":
            rejected.append(f"{filename} (status: {status})")

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean configs were incorrectly rejected:\n" + "\n".join(rejected))