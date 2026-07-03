# test_final_state.py
import os
import subprocess
import glob
import pytest

VALIDATOR_SCRIPT = "/home/user/build_validator.py"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_validator_script_exists():
    """Ensure the student created the build_validator.py script."""
    assert os.path.isfile(VALIDATOR_SCRIPT), f"Validator script not found at {VALIDATOR_SCRIPT}"

def test_clean_corpus():
    """
    Iterate over every file in the clean corpus path.
    Assert the agent's solution accepts each one (exit code 0, prints VALID).
    """
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*"))
    assert len(clean_files) > 0, f"No files found in clean corpus directory {CLEAN_DIR}"

    failures = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", VALIDATOR_SCRIPT, filepath], 
            capture_output=True, 
            text=True
        )

        # Check if it exits with 0 and prints "VALID"
        if result.returncode != 0 or "VALID" not in result.stdout.strip().upper():
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean modified/rejected: {', '.join(failures)}")

def test_evil_corpus():
    """
    Iterate over every file in the evil corpus path.
    Assert the agent's solution rejects each one (exit code 1, prints INVALID).
    """
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*"))
    assert len(evil_files) > 0, f"No files found in evil corpus directory {EVIL_DIR}"

    failures = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", VALIDATOR_SCRIPT, filepath], 
            capture_output=True, 
            text=True
        )

        # Check if it exits with 1 and prints "INVALID"
        if result.returncode != 1 or "INVALID" not in result.stdout.strip().upper():
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil bypassed: {', '.join(failures)}")