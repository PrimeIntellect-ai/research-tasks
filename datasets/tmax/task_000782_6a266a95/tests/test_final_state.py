# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_cgraph_built():
    assert os.path.isfile("/app/cgraph-1.0/libcgraph.a"), "The library /app/cgraph-1.0/libcgraph.a was not built."

def test_executable_exists():
    executable = "/home/user/deadlock_detector"
    assert os.path.isfile(executable), f"The executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"The file {executable} is not executable."

def test_adversarial_corpus():
    executable = "/home/user/deadlock_detector"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, f"No files found in {evil_dir}"
    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        result = subprocess.run([executable, f], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    for f in clean_files:
        result = subprocess.run([executable, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))