# test_final_state.py

import os

def test_bad_commit_file_exists():
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. You must write the bad commit hash to this file."

def test_bad_commit_hash_correct():
    submit_path = "/home/user/bad_commit.txt"
    truth_path = "/tmp/ground_truth_commit.txt"

    assert os.path.isfile(submit_path), f"Missing {submit_path}"
    assert os.path.isfile(truth_path), f"Missing {truth_path} (internal error)"

    with open(submit_path, "r") as f:
        submitted_hash = f.read().strip()

    with open(truth_path, "r") as f:
        truth_hash = f.read().strip()

    assert submitted_hash == truth_hash, (
        f"The commit hash in {submit_path} is incorrect.\n"
        f"Expected: {truth_hash}\n"
        f"Found:    {submitted_hash}"
    )