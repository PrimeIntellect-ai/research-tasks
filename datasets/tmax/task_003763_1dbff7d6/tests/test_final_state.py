# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit_query.py"
CLEAN_DIR = "/app/tests/clean/"
EVIL_DIR = "/app/tests/evil/"

def test_script_exists():
    """Verify that the agent created the audit script."""
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

def test_clean_corpus():
    """Verify that the script accepts all clean queries."""
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.cypher"))
    assert len(clean_files) > 0, f"No clean files found in {CLEAN_DIR}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean queries rejected/modified incorrectly. Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    """Verify that the script rejects all evil queries."""
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.cypher"))
    assert len(evil_files) > 0, f"No evil files found in {EVIL_DIR}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, filepath],
            capture_output=True,
            text=True
        )
        if result.returncode != 1 or "REJECT" not in result.stdout:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil queries bypassed the filter. Offending files: {', '.join(failed_files)}")