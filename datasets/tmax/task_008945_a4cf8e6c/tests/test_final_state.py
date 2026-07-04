# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash_identified():
    bad_commit_path = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist."

    with open(bad_commit_path, "r") as f:
        commit_hash = f.read().strip()

    assert len(commit_hash) == 40, f"Expected a 40-character commit hash, got '{commit_hash}' (length {len(commit_hash)})."

    repo_path = "/home/user/db-exporter"
    try:
        result = subprocess.run(
            ["git", "log", "--format=%s", "-n", "1", commit_hash],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        commit_message = result.stdout.strip()
        assert commit_message == "Commit 137", f"The identified commit is '{commit_message}', expected 'Commit 137'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to retrieve git commit message for hash {commit_hash}: {e.stderr}")

def test_output_bin_matches_expected():
    expected_bin_path = "/home/user/expected.bin"
    output_bin_path = "/home/user/db-exporter/output.bin"

    assert os.path.isfile(expected_bin_path), f"File {expected_bin_path} does not exist."
    assert os.path.isfile(output_bin_path), f"File {output_bin_path} does not exist. Did you run the export command?"

    with open(expected_bin_path, "rb") as f:
        expected_data = f.read()

    with open(output_bin_path, "rb") as f:
        output_data = f.read()

    assert output_data == expected_data, f"The generated {output_bin_path} does not match {expected_bin_path}."