# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_filter_go_exists():
    assert os.path.isfile("/home/user/filter.go"), "/home/user/filter.go does not exist."

def test_clean_corpus():
    clean_files = glob.glob("/app/corpus/clean/*.nc")
    assert len(clean_files) > 0, "No clean files found in /app/corpus/clean/"

    failures = []
    for filepath in clean_files:
        result = subprocess.run(
            ["go", "run", "/home/user/filter.go", filepath],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files modified/rejected incorrectly: {', '.join(failures)}")

def test_evil_corpus():
    evil_files = glob.glob("/app/corpus/evil/*.nc")
    assert len(evil_files) > 0, "No evil files found in /app/corpus/evil/"

    failures = []
    for filepath in evil_files:
        result = subprocess.run(
            ["go", "run", "/home/user/filter.go", filepath],
            capture_output=True,
            text=True
        )
        if result.returncode != 1:
            failures.append(os.path.basename(filepath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed/accepted incorrectly: {', '.join(failures)}")