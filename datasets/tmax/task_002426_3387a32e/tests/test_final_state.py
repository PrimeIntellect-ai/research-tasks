# test_final_state.py

import os
import subprocess
import pytest

def test_triage_logs_binary_exists():
    binary_path = "/home/user/triage_logs"
    assert os.path.isfile(binary_path), f"Missing binary file: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary file is not executable: {binary_path}"

def test_adversarial_corpus():
    binary_path = "/home/user/triage_logs"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".csv")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".csv")]

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    clean_failures = []
    evil_failures = []

    for fpath in clean_files:
        result = subprocess.run([binary_path, fpath], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            clean_failures.append((os.path.basename(fpath), result.returncode, output))

    for fpath in evil_files:
        result = subprocess.run([binary_path, fpath], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "EVIL":
            evil_failures.append((os.path.basename(fpath), result.returncode, output))

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected.")
        for name, code, out in clean_failures:
            error_msg.append(f"  - {name} (code: {code}, output: {out})")

    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed.")
        for name, code, out in evil_failures:
            error_msg.append(f"  - {name} (code: {code}, output: {out})")

    if error_msg:
        pytest.fail("\n".join(error_msg))