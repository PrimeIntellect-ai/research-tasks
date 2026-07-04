# test_final_state.py

import os
import subprocess
import pytest

def test_failed_jobs_txt():
    expected_jobs = ["1012", "1045", "1099"]
    target_file = "/home/user/failed_jobs.txt"

    assert os.path.exists(target_file), f"{target_file} does not exist."

    with open(target_file, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_jobs, f"Expected {expected_jobs} in {target_file}, but got {content}."

def test_job_filter_script():
    filter_script = "/home/user/job_filter.py"
    assert os.path.exists(filter_script), f"{filter_script} does not exist."

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"{evil_dir} does not exist."
    assert os.path.isdir(clean_dir), f"{clean_dir} does not exist."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        with open(evil_file, "r") as f:
            test_input = f.read()

        # Run the script
        result = subprocess.run(
            ["python3", filter_script, test_input],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if output != "REJECT" or result.returncode != 1:
            evil_bypassed.append((os.path.basename(evil_file), output, result.returncode))

    for clean_file in clean_files:
        with open(clean_file, "r") as f:
            test_input = f.read()

        # Run the script
        result = subprocess.run(
            ["python3", filter_script, test_input],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if output != "ACCEPT" or result.returncode != 0:
            clean_modified.append((os.path.basename(clean_file), output, result.returncode))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {[f[0] for f in evil_bypassed]}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {[f[0] for f in clean_modified]}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msgs)