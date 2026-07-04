# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_cjson_build_and_test():
    """Verify that cJSON compiles and its tests pass."""
    cwd = "/app/vendored/cJSON"

    # Run make clean
    subprocess.run(["make", "clean"], cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Run make all
    make_all = subprocess.run(["make", "all"], cwd=cwd, capture_output=True, text=True)
    assert make_all.returncode == 0, f"'make all' failed in {cwd}:\n{make_all.stderr}"

    # Run tests
    test_run = subprocess.run(["./cJSON_test"], cwd=cwd, capture_output=True, text=True)
    assert test_run.returncode == 0, f"'./cJSON_test' failed in {cwd}:\n{test_run.stderr}"

def test_filter_script_exists_and_executable():
    """Verify that the filter script exists and is executable."""
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Filter script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Filter script at {script_path} is not executable"

def test_filter_script_clean_corpus():
    """Verify that the filter script accepts all clean files."""
    script_path = "/home/user/filter.sh"
    clean_dir = "/app/corpora/clean"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_filter_script_evil_corpus():
    """Verify that the filter script rejects all evil files."""
    script_path = "/home/user/filter.sh"
    evil_dir = "/app/corpora/evil"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    failed_files = []
    for f in evil_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(failed_files)}")