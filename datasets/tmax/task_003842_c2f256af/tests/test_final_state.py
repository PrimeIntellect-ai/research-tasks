# test_final_state.py

import os
import subprocess
import pytest

def get_expected_key():
    try:
        pid = subprocess.check_output(["pgrep", "-f", "suspicious_daemon"]).decode().strip()
    except subprocess.CalledProcessError:
        pytest.fail("suspicious_daemon process is not running, cannot verify the expected key.")

    fd_dir = f"/proc/{pid}/fd"
    for fd in os.listdir(fd_dir):
        fd_path = os.path.join(fd_dir, fd)
        try:
            link = os.readlink(fd_path)
            if "secret_key.txt" in link:
                with open(fd_path, "r") as f:
                    return f.read().strip()
        except Exception:
            continue
    pytest.fail("Could not find the deleted secret_key.txt in the daemon's file descriptors.")

def get_expected_commit():
    repo_dir = "/home/user/daemon_src"
    try:
        output = subprocess.check_output(
            ["git", "log", "-S", "static mut IS_AUTH", "--format=%H", "--reverse"],
            cwd=repo_dir,
            stderr=subprocess.DEVNULL
        ).decode().strip()
        if not output:
            pytest.fail("Could not find the bad commit in git history.")
        return output.split('\n')[0].strip()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute git command to find the bad commit.")

def test_recovered_key():
    """Test that the recovered key matches the original secret key."""
    expected_key = get_expected_key()

    recovered_key_path = "/home/user/recovered_key.txt"
    assert os.path.isfile(recovered_key_path), f"File {recovered_key_path} does not exist."

    with open(recovered_key_path, "r") as f:
        recovered_key = f.read().strip()

    assert recovered_key == expected_key, "The recovered key does not match the expected secret key."

def test_bad_commit():
    """Test that the bad commit hash matches the commit that introduced the vulnerability."""
    expected_commit = get_expected_commit()

    bad_commit_path = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist."

    with open(bad_commit_path, "r") as f:
        bad_commit = f.read().strip()

    assert bad_commit == expected_commit, "The bad commit hash does not match the expected commit."