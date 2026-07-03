# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_env_setup():
    script_path = "/home/user/env_setup.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"

    # Source the script and print the variable
    cmd = f"source {script_path} && echo -n $QA_TEST_SEED"
    result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)

    assert result.returncode == 0, f"Failed to source {script_path}. Stderr: {result.stderr}"
    assert result.stdout == "8472", f"Expected QA_TEST_SEED=8472, got {result.stdout!r}"

def test_math_filter_executable():
    script_path = "/home/user/math_filter.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_math_filter_adversarial():
    script_path = "/home/user/math_filter.sh"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_failed = []
    for f in clean_files:
        res = subprocess.run([script_path, f], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run([script_path, f], capture_output=True)
        # Evil files must be rejected (exit code 1 or at least non-zero)
        # The prompt specifies "exit code 1", but any non-zero usually indicates rejection.
        # We will check specifically for 0 as a bypass.
        if res.returncode == 0:
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not error_msgs, " | ".join(error_msgs)