# test_final_state.py

import os
import glob
import subprocess
import json
import pytest

def test_filter_clean_corpus():
    """
    Iterate over every file in the clean corpus path and assert the agent's
    solution accepts it (exit code 0).
    """
    clean_dir = "/home/user/sim_data/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.npy"))
    assert len(clean_files) > 0, f"No clean files found in {clean_dir}."

    failed_files = []
    for f in clean_files:
        result = subprocess.run(["python3", "/home/user/filter.py", f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, (
        f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected "
        f"(expected exit code 0). Offending files: {failed_files[:10]}"
    )

def test_filter_evil_corpus():
    """
    Iterate over every file in the evil corpus path and assert the agent's
    solution rejects it (exit code 1).
    """
    evil_dir = "/home/user/sim_data/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.npy"))
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}."

    failed_files = []
    for f in evil_files:
        result = subprocess.run(["python3", "/home/user/filter.py", f], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(f))

    assert not failed_files, (
        f"{len(failed_files)} of {len(evil_files)} evil files bypassed "
        f"(expected exit code 1). Offending files: {failed_files[:10]}"
    )

def test_pipeline_registration_log():
    """
    Assert that /home/user/registered.log exists, contains exactly 10 clean file IDs,
    and contains no evil file IDs.
    """
    log_path = "/home/user/registered.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. The pipeline likely failed to run or register files."

    with open(log_path, "r") as f:
        content = f.read().strip()

    lines = [line for line in content.split("\n") if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 registered files in {log_path}, found {len(lines)}."

    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse line as JSON in {log_path}: {line}")

        file_id = data.get("file_id", "")
        status = data.get("status", "")

        assert "evil" not in file_id.lower(), f"An evil file ID ('{file_id}') was improperly registered in the log!"
        assert "clean" in file_id.lower(), f"Unrecognized file ID format ('{file_id}') registered."
        assert status == "clean", f"Expected status 'clean' in payload, got '{status}'."