# test_final_state.py

import os
import subprocess
import pytest
import shutil

REPO_DIR = "/home/user/asset_processor"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
EXPECTED_BAD_COMMIT_FILE = "/tmp/expected_bad_commit.txt"
PATCH_FILE = "/home/user/fix.patch"

def test_bad_commit_identified():
    assert os.path.isfile(BAD_COMMIT_FILE), f"The file {BAD_COMMIT_FILE} does not exist."
    assert os.path.isfile(EXPECTED_BAD_COMMIT_FILE), f"The expected truth file {EXPECTED_BAD_COMMIT_FILE} is missing."

    with open(BAD_COMMIT_FILE, "r") as f:
        actual_hash = f.read().strip()

    with open(EXPECTED_BAD_COMMIT_FILE, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Incorrect bad commit identified. Expected '{expected_hash}', but got '{actual_hash}'."

def test_fix_patch_exists():
    assert os.path.isfile(PATCH_FILE), f"The patch file {PATCH_FILE} does not exist."
    assert os.path.getsize(PATCH_FILE) > 0, f"The patch file {PATCH_FILE} is empty."

    with open(PATCH_FILE, "r") as f:
        content = f.read()
    assert "diff" in content or "---" in content, f"The file {PATCH_FILE} does not appear to be a valid patch."

def test_script_handles_spaces_correctly():
    script_path = os.path.join(REPO_DIR, "build_and_process.sh")
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    test_dir = "/tmp/test dir"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    test_file = os.path.join(test_dir, "file with spaces.txt")
    with open(test_file, "w") as f:
        f.write("dummy content")

    result = subprocess.run(
        [script_path, test_dir],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    expected_output = f"Processed: {test_file}"
    assert expected_output in result.stdout, (
        f"The script did not correctly process the file with spaces.\n"
        f"Expected output to contain: '{expected_output}'\n"
        f"Actual output:\n{result.stdout}"
    )

    # Cleanup
    shutil.rmtree(test_dir)