# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_txt():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(actual_file), f"{actual_file} does not exist."
    assert os.path.isfile(expected_file), f"{expected_file} does not exist. (Setup issue)"

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {actual_file} ({actual_hash}) does not match the expected bad commit ({expected_hash})."

def test_git_branch_main():
    repo_dir = "/home/user/tz_utils"
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to get current git branch."
    current_branch = result.stdout.strip()
    assert current_branch == "main", f"Expected to be on 'main' branch, but currently on '{current_branch}'."

def test_fuzz_test_passes():
    repo_dir = "/home/user/tz_utils"

    # Run the fuzz test with a small number of runs to ensure it passes without panics
    env = os.environ.copy()
    env["PATH"] = f"{os.environ.get('HOME', '/root')}/.cargo/bin:{env.get('PATH', '')}"

    result = subprocess.run(
        ["cargo", "+nightly", "fuzz", "run", "fuzz_target_1", "--", "-runs=1000"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        env=env
    )

    assert result.returncode == 0, f"Fuzz test failed or panicked. Stderr:\n{result.stderr}\nStdout:\n{result.stdout}"

def test_working_tree_clean():
    repo_dir = "/home/user/tz_utils"
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run git status."
    assert result.stdout.strip() == "", "Working tree is not clean. Ensure your fix is committed."