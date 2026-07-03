# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_executable_exists():
    executable = "/app/build/validator"
    assert os.path.isfile(executable), f"Executable {executable} not found."
    assert os.access(executable, os.X_OK), f"Executable {executable} is not executable."

def test_clean_corpus():
    executable = "/app/build/validator"
    clean_files = glob.glob("/app/corpus/clean/*.bin")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        res = subprocess.run([executable, f], capture_output=True)
        if res.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    executable = "/app/build/validator"
    evil_files = glob.glob("/app/corpus/evil/*.bin")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for f in evil_files:
        res = subprocess.run([executable, f], capture_output=True)
        if res.returncode == 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(failed_files)}")