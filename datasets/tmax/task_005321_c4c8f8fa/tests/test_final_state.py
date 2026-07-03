# test_final_state.py
import os
import subprocess
import pytest

def test_verifier_exists():
    verifier_path = "/home/user/verifier"
    assert os.path.isfile(verifier_path), f"Verifier executable {verifier_path} is missing."
    assert os.access(verifier_path, os.X_OK), f"Verifier {verifier_path} is not executable."

def test_clean_corpus():
    clean_dir = "/app/corpus/clean"
    verifier_path = "/home/user/verifier"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    clean_files = sorted([f for f in os.listdir(clean_dir) if f.endswith(".h5")])
    assert len(clean_files) > 0, "No clean .h5 files found."

    failed_files = []

    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        result = subprocess.run([verifier_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(failed_files)}"

def test_evil_corpus():
    evil_dir = "/app/corpus/evil"
    verifier_path = "/home/user/verifier"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."
    evil_files = sorted([f for f in os.listdir(evil_dir) if f.endswith(".h5")])
    assert len(evil_files) > 0, "No evil .h5 files found."

    bypassed_files = []

    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        result = subprocess.run([verifier_path, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(f)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(bypassed_files)}"