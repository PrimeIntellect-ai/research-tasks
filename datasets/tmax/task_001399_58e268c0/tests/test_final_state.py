# test_final_state.py

import os
import subprocess
import pytest

def get_expected_crash_tx():
    dump_path = "/app/memory.dmp"
    if not os.path.exists(dump_path):
        pytest.fail(f"Memory dump missing at {dump_path}")
    with open(dump_path, "rb") as f:
        content = f.read()
        idx = content.find(b"CRASH_TX:")
        if idx != -1:
            return content[idx+9:idx+9+32].decode("ascii")
    pytest.fail("Could not find CRASH_TX in memory dump.")

def test_crash_tx_extracted():
    expected_tx = get_expected_crash_tx()
    out_path = "/home/user/crash_tx.txt"
    assert os.path.isfile(out_path), f"File {out_path} is missing."

    with open(out_path, "r") as f:
        actual_tx = f.read().strip()

    assert actual_tx == expected_tx, f"Expected crash TX '{expected_tx}', but got '{actual_tx}' in {out_path}."

def test_sanitiser_executable_exists():
    exe_path = "/home/user/sanitiser"
    assert os.path.isfile(exe_path), f"Sanitiser executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"Sanitiser {exe_path} is not executable."

def test_sanitiser_on_corpora():
    exe_path = "/home/user/sanitiser"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    assert os.path.isfile(exe_path), "Sanitiser executable not found."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run([exe_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run([exe_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))