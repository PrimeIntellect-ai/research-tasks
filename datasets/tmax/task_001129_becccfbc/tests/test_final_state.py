# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_cmake_fixed():
    cmake_path = "/app/csv-parser/CMakeLists.txt"
    assert os.path.isfile(cmake_path), f"File missing: {cmake_path}"

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "set(CMAKE_CXX_STANDARD 17)" in content, "CMakeLists.txt was not fixed to require C++17."

def test_run_filter_exists_and_executable():
    script_path = "/home/user/run_filter.sh"
    assert os.path.isfile(script_path), f"File missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_adversarial_corpus_evaluation():
    script_path = "/home/user/run_filter.sh"

    evil_dir = "/app/data/evil"
    clean_dir = "/app/data/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(evil_files) > 0, "Evil corpus is missing."
    assert len(clean_files) > 0, "Clean corpus is missing."

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run([script_path, f], capture_output=True)
        # Expected exit code 1 for EVIL
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run([script_path, f], capture_output=True)
        # Expected exit code 0 for CLEAN
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))