# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect_deadlocks.sh"

def run_script(filepath):
    """Helper to run the bash script on a given file and return stdout and exit code."""
    try:
        result = subprocess.run(
            ["bash", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception as e:
        return str(e), -1

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing: {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK) or os.access(SCRIPT_PATH, os.R_OK), f"Script not executable/readable: {SCRIPT_PATH}"

def test_evil_corpus():
    """Test that all files in the evil corpus output DEADLOCK and exit with 0."""
    evil_dir = "/app/corpus/evil"
    csv_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    assert len(csv_files) > 0, "No files found in evil corpus."

    failures = []
    for filepath in csv_files:
        out, code = run_script(filepath)
        if out != "DEADLOCK" or code != 0:
            failures.append(f"{os.path.basename(filepath)} (out: {out}, code: {code})")

    assert not failures, f"{len(failures)} of {len(csv_files)} evil bypassed: {', '.join(failures[:10])}"

def test_clean_corpus():
    """Test that all files in the clean corpus output VALID and exit with 0."""
    clean_dir = "/app/corpus/clean"
    csv_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    assert len(csv_files) > 0, "No files found in clean corpus."

    failures = []
    for filepath in csv_files:
        out, code = run_script(filepath)
        if out != "VALID" or code != 0:
            failures.append(f"{os.path.basename(filepath)} (out: {out}, code: {code})")

    assert not failures, f"{len(failures)} of {len(csv_files)} clean modified/failed: {', '.join(failures[:10])}"

def test_invalid_corpus():
    """Test that all files in the invalid corpus output INVALID_SCHEMA and exit with 1."""
    invalid_dir = "/app/corpus/invalid"
    csv_files = glob.glob(os.path.join(invalid_dir, "*.csv"))
    assert len(csv_files) > 0, "No files found in invalid corpus."

    failures = []
    for filepath in csv_files:
        out, code = run_script(filepath)
        if out != "INVALID_SCHEMA" or code != 1:
            failures.append(f"{os.path.basename(filepath)} (out: {out}, code: {code})")

    assert not failures, f"{len(failures)} of {len(csv_files)} invalid bypassed: {', '.join(failures[:10])}"