# test_final_state.py

import os
import struct
import subprocess

def test_bad_commit_txt():
    bad_commit_path = "/home/user/bad_commit.txt"
    expected_path = "/tmp/expected_bad_commit.txt"

    assert os.path.exists(bad_commit_path), f"File {bad_commit_path} does not exist."
    assert os.path.exists(expected_path), f"File {expected_path} does not exist."

    with open(bad_commit_path, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash '{expected_hash}', but got '{actual_hash}'."

def test_mre_bin():
    mre_path = "/home/user/mre.bin"
    assert os.path.exists(mre_path), f"File {mre_path} does not exist."

    with open(mre_path, "rb") as f:
        data = f.read()

    assert len(data) == 8, f"Expected {mre_path} to be exactly 8 bytes, but got {len(data)} bytes."

    sensor_id, sensor_value = struct.unpack("<II", data)

    assert sensor_id != 0, "Sensor ID (first 4 bytes) must be non-zero."
    assert sensor_value == 0x7FFFFFFF, f"Sensor value (last 4 bytes) must be 0x7FFFFFFF, but got 0x{sensor_value:08X}."

def test_mre_triggers_segfault():
    expected_path = "/tmp/expected_bad_commit.txt"
    assert os.path.exists(expected_path), f"File {expected_path} does not exist."

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    repo_dir = "/home/user/telemetry_decoder"
    mre_path = "/home/user/mre.bin"

    assert os.path.exists(repo_dir), f"Directory {repo_dir} does not exist."
    assert os.path.exists(mre_path), f"File {mre_path} does not exist."

    # Checkout bad commit
    checkout_proc = subprocess.run(["git", "checkout", expected_hash], cwd=repo_dir, capture_output=True)
    assert checkout_proc.returncode == 0, f"Failed to checkout bad commit {expected_hash}."

    try:
        # Compile
        compile_proc = subprocess.run(["gcc", "main.c", "-o", "decoder"], cwd=repo_dir, capture_output=True)
        assert compile_proc.returncode == 0, "Failed to compile main.c at the bad commit."

        # Run
        with open(mre_path, "rb") as f:
            run_proc = subprocess.run(["./decoder"], cwd=repo_dir, stdin=f, capture_output=True)

        # Segfault is usually indicated by a negative signal (-11) or shell exit code (139)
        assert run_proc.returncode in (-11, 139), f"Expected segmentation fault (return code -11 or 139), but got {run_proc.returncode}."
    finally:
        # Restore git state
        subprocess.run(["git", "checkout", "master"], cwd=repo_dir, capture_output=True)