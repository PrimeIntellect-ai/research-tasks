# test_final_state.py

import os
import time
import subprocess
import pytest

def test_curator_binary_exists():
    """Verify that the curator binary was compiled and is executable."""
    binary_path = "/home/user/curator"
    assert os.path.exists(binary_path), f"The binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The binary {binary_path} is not executable."

def test_curator_running():
    """Verify that the curator daemon is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "curator"]).decode()
        assert output.strip() != "", "The curator process is not running in the background."
    except subprocess.CalledProcessError:
        pytest.fail("The curator process is not running in the background.")

def test_curator_processing():
    """Verify the daemon correctly processes a new file."""
    test_filename = "pytest_artifact.bin"
    incoming_path = f"/home/user/repo/incoming/{test_filename}"

    # Generate 512KB of random data
    data = os.urandom(512 * 1024)
    checksum = sum(data) & 0xFFFFFFFF
    expected_checksum = f"{checksum:08x}"

    # Write the file to trigger inotify IN_CLOSE_WRITE
    with open(incoming_path, "wb") as f:
        f.write(data)

    # Give the daemon time to process the file
    time.sleep(3)

    # 1. Verify original file is deleted
    assert not os.path.exists(incoming_path), f"Original file {incoming_path} was not deleted from incoming directory."

    # 2. Verify object file is created with correct checksum
    object_path = f"/home/user/repo/objects/{expected_checksum}"
    assert os.path.exists(object_path), f"Object file {object_path} was not created. Expected checksum: {expected_checksum}"

    with open(object_path, "rb") as f:
        assert f.read() == data, "The contents of the object file do not match the original data."

    # 3. Verify symlink is created
    symlink_path = f"/home/user/repo/by-name/{test_filename}"
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} was not created."

    target = os.readlink(symlink_path)
    expected_target = f"../objects/{expected_checksum}"
    assert target == expected_target, f"Symlink points to '{target}', expected '{expected_target}'."

    # 4. Verify latest.txt is updated
    latest_path = "/home/user/repo/latest.txt"
    assert os.path.exists(latest_path), f"File {latest_path} does not exist."

    with open(latest_path, "r") as f:
        latest = f.read()
    assert latest == f"{expected_checksum}\n", f"latest.txt contains {repr(latest)}, expected {repr(expected_checksum + chr(10))}."