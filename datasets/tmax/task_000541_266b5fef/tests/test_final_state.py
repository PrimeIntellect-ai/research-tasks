# test_final_state.py

import os
import subprocess
import pytest
import glob

def test_audit_filter_exists():
    script_path = "/home/user/audit_filter.py"
    assert os.path.isfile(script_path), f"The required script {script_path} does not exist."

def test_audit_filter_clean_corpus():
    script_path = "/home/user/audit_filter.py"
    clean_dir = "/home/user/corpora/clean/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."

    failed_files = []

    for file_path in clean_files:
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if output != "ACCEPT":
            failed_files.append((os.path.basename(file_path), output, result.stderr.strip()))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean files rejected or failed.\n"
        for fname, out, err in failed_files[:5]:
            error_msg += f"  {fname}: expected ACCEPT, got {repr(out)}\n"
        if len(failed_files) > 5:
            error_msg += "  ...\n"
        pytest.fail(error_msg)

def test_audit_filter_evil_corpus():
    script_path = "/home/user/audit_filter.py"
    evil_dir = "/home/user/corpora/evil/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    failed_files = []

    for file_path in evil_files:
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if output != "REJECT":
            failed_files.append((os.path.basename(file_path), output, result.stderr.strip()))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil files bypassed or failed.\n"
        for fname, out, err in failed_files[:5]:
            error_msg += f"  {fname}: expected REJECT, got {repr(out)}\n"
        if len(failed_files) > 5:
            error_msg += "  ...\n"
        pytest.fail(error_msg)