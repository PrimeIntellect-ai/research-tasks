# test_final_state.py

import os
import subprocess
import pytest

def run_validator(filepath):
    script_path = "/home/user/validator.py"
    assert os.path.isfile(script_path), f"Validator script missing at {script_path}"

    result = subprocess.run(
        ["python3", script_path, filepath],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_clean_corpus_accepted():
    clean_dir = "/app/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(files) > 0, f"Clean corpus directory is empty: {clean_dir}"

    failed_files = []
    for f in files:
        filepath = os.path.join(clean_dir, f)
        output = run_validator(filepath)
        if output != "ACCEPT":
            failed_files.append((f, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} clean files were not ACCEPTED.\n"
        error_msg += "Offending files:\n"
        for f, out in failed_files[:5]:
            error_msg += f" - {f} (Output: {out})\n"
        pytest.fail(error_msg)

def test_evil_corpus_rejected():
    evil_dir = "/app/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(files) > 0, f"Evil corpus directory is empty: {evil_dir}"

    failed_files = []
    for f in files:
        filepath = os.path.join(evil_dir, f)
        output = run_validator(filepath)
        if output != "REJECT":
            failed_files.append((f, output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(files)} evil files bypassed rejection.\n"
        error_msg += "Offending files:\n"
        for f, out in failed_files[:5]:
            error_msg += f" - {f} (Output: {out})\n"
        pytest.fail(error_msg)