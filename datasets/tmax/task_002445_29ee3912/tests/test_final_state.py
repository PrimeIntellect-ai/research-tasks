# test_final_state.py

import os
import subprocess
import pytest

def test_resolution_file_exists_and_content():
    resolution_path = "/home/user/resolution.txt"
    assert os.path.isfile(resolution_path), f"Resolution file not found at {resolution_path}"

    with open(resolution_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {resolution_path}, found {len(lines)}"

    bad_commit_hash_path = "/tmp/bad_commit_hash.txt"
    assert os.path.isfile(bad_commit_hash_path), "Truth file /tmp/bad_commit_hash.txt is missing"

    with open(bad_commit_hash_path, "r") as f:
        expected_hash = f.read().strip()

    assert lines[0] == expected_hash, f"Line 1 (commit hash): Expected '{expected_hash}', got '{lines[0]}'"
    assert lines[1] == "10050000.00", f"Line 2 (output): Expected '10050000.00', got '{lines[1]}'"

def test_go_code_fixed_and_tests_pass():
    repo_path = "/home/user/fin-aggregator"
    assert os.path.isdir(repo_path), f"Repository directory not found at {repo_path}"

    try:
        subprocess.run(
            ["go", "test"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"The Go test suite is still failing. The bug in aggregator.go was not properly fixed.\nOutput:\n{e.output}")