# test_final_state.py

import os
import subprocess

def test_bad_commit_identified():
    secret_file = "/home/user/.secret_expected_bad_commit"
    user_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(user_file), f"The file {user_file} does not exist."

    with open(secret_file, "r") as f:
        expected_commit = f.read().strip()

    with open(user_file, "r") as f:
        user_commit = f.read().strip()

    assert user_commit == expected_commit, (
        f"The commit hash in {user_file} is incorrect. "
        f"Expected {expected_commit}, but got {user_commit}."
    )

def test_leak_script_passes():
    script_path = "/home/user/test_leak.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

    # Run the test script
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"The test script {script_path} failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n"
        "This indicates either the environment is still misconfigured or the memory leak is not fixed."
    )
    assert "No leak detected" in result.stdout, "The output did not confirm that no leak was detected."

def test_fix_patch_exists_and_valid():
    patch_path = "/home/user/fix.patch"
    assert os.path.isfile(patch_path), f"The patch file {patch_path} is missing."

    with open(patch_path, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, (
        f"The file {patch_path} does not appear to be a valid unified diff patch."
    )