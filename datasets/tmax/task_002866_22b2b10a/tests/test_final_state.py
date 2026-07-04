# test_final_state.py

import os
import subprocess
import pytest

def test_classifier_executable_exists():
    executable = "/home/user/classifier"
    assert os.path.isfile(executable), f"Executable {executable} does not exist. Did you compile your tool?"
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_adversarial_corpus():
    executable = "/home/user/classifier"
    clean_dir = "/app/hidden_corpus/clean"
    evil_dir = "/app/hidden_corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus dir {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus dir {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed_clean = []
    failed_evil = []

    for cf in clean_files:
        result = subprocess.run([executable, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([executable, ef], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {', '.join(failed_clean[:10])}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(failed_evil[:10])}")

    assert not failed_clean and not failed_evil, " | ".join(error_msgs)

def test_libelfval_built():
    lib_path = "/app/simple-elf-validator-0.1.0/libelfval.a"
    assert os.path.isfile(lib_path), f"Static library {lib_path} does not exist. Did you fix the Makefile and run make?"