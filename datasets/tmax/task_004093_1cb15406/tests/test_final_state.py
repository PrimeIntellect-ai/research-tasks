# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_filter_data_script():
    script_path = "/home/user/filter_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.R_OK), f"Script {script_path} is not readable."

    clean_files = glob.glob("/app/data/clean/*.csv")
    evil_files = glob.glob("/app/data/evil/*.csv")

    assert len(clean_files) > 0, "No clean files found in /app/data/clean/"
    assert len(evil_files) > 0, "No evil files found in /app/data/evil/"

    clean_failed = []
    for f in clean_files:
        result = subprocess.run(["bash", script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_passed = []
    for f in evil_files:
        result = subprocess.run(["bash", script_path, f], capture_output=True)
        # The script should exit with 1 if it violates ANY rule.
        # So a return code of 0 means it bypassed the checks.
        if result.returncode == 0:
            evil_passed.append(os.path.basename(f))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_passed:
        error_msgs.append(f"{len(evil_passed)} of {len(evil_files)} evil bypassed: {', '.join(evil_passed)}")

    assert not clean_failed and not evil_passed, " | ".join(error_msgs)