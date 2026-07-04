# test_final_state.py

import os

def test_bad_commit_hash():
    user_file = "/home/user/bad_commit.txt"
    truth_file = "/tmp/true_bad_commit.txt"

    assert os.path.isfile(user_file), f"The file {user_file} was not created."
    assert os.path.isfile(truth_file), f"The truth file {truth_file} is missing from the environment."

    with open(user_file, "r") as f:
        user_hash = f.read().strip()

    with open(truth_file, "r") as f:
        true_hash = f.read().strip()

    assert user_hash == true_hash, f"Incorrect bad commit hash. Expected '{true_hash}', but got '{user_hash}' in {user_file}."

def test_expected_rate():
    rate_file = "/home/user/expected_rate.txt"

    assert os.path.isfile(rate_file), f"The file {rate_file} was not created."

    with open(rate_file, "r") as f:
        rate = f.read().strip()

    assert rate == "0.5", f"Incorrect expected rate. Expected '0.5', but got '{rate}' in {rate_file}."