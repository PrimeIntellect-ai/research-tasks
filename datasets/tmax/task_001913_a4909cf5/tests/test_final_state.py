# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_txt_exists_and_correct():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_commit_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist."
    assert os.path.isfile(expected_commit_file), f"File {expected_commit_file} is missing."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_commit_file, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, (
        f"The commit hash in {bad_commit_file} is incorrect. "
        f"Expected {expected_commit}, got {actual_commit}."
    )

def test_build_passes():
    repo_dir = "/home/user/app_repo"
    build_script = "./build.sh"

    assert os.path.isdir(repo_dir), f"Directory {repo_dir} does not exist."
    assert os.path.isfile(os.path.join(repo_dir, "build.sh")), f"Build script {build_script} is missing."

    result = subprocess.run(
        [build_script],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"The build script failed with return code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )
    assert "Build and tests passed." in result.stdout, (
        "The build script did not output the expected success message."
    )

def test_process_c_fixed():
    process_c_file = "/home/user/app_repo/process.c"
    assert os.path.isfile(process_c_file), f"File {process_c_file} is missing."

    with open(process_c_file, "r") as f:
        content = f.read()

    # The bug was `i <= count`. It should be fixed to not include the out-of-bounds index.
    # While the build passing is the primary test, we can also assert the off-by-one is gone.
    assert "i <= count" not in content, (
        "The off-by-one error (i <= count) is still present in process.c."
    )