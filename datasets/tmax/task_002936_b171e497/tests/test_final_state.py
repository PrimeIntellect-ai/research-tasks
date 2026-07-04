# test_final_state.py

import os
import subprocess
import pytest

def test_audit_classifier_exists():
    """Verify that the agent created the audit_classifier.py script."""
    script_path = "/home/user/audit_classifier.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}."

def test_audit_classifier_evil_corpus():
    """Verify that the script correctly flags all evil databases as VIOLATION."""
    script_path = "/home/user/audit_classifier.py"
    evil_dir = "/app/corpora/evil/"

    result = subprocess.run(
        ["python3", script_path, evil_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    db_files = [f for f in os.listdir(evil_dir) if f.endswith('.db')]

    failed_files = []
    for db_file in db_files:
        expected_output = f"{db_file}: VIOLATION"
        if expected_output not in output_lines:
            failed_files.append(db_file)

    assert not failed_files, f"{len(failed_files)} of {len(db_files)} evil bypassed. Offending files: {', '.join(failed_files)}"

def test_audit_classifier_clean_corpus():
    """Verify that the script correctly flags all clean databases as CLEAN."""
    script_path = "/home/user/audit_classifier.py"
    clean_dir = "/app/corpora/clean/"

    result = subprocess.run(
        ["python3", script_path, clean_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    db_files = [f for f in os.listdir(clean_dir) if f.endswith('.db')]

    failed_files = []
    for db_file in db_files:
        expected_output = f"{db_file}: CLEAN"
        if expected_output not in output_lines:
            failed_files.append(db_file)

    assert not failed_files, f"{len(failed_files)} of {len(db_files)} clean modified (flagged incorrectly). Offending files: {', '.join(failed_files)}"