# test_final_state.py

import os
import pytest

def test_recovered_seed():
    seed_file = "/home/user/recovered_seed.txt"
    assert os.path.isfile(seed_file), f"File {seed_file} does not exist. You must save the recovered seed to this file."

    with open(seed_file, "r") as f:
        seed_value = f.read().strip()

    assert seed_value == "849302", f"The recovered seed in {seed_file} is incorrect. Expected '849302', got '{seed_value}'."

def test_bad_commit_hash():
    hash_file = "/home/user/bad_commit_hash.txt"
    truth_file = "/tmp/truth/expected_bad_commit.txt"

    assert os.path.isfile(hash_file), f"File {hash_file} does not exist. You must save the bad commit hash to this file."
    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing. The environment is corrupted."

    with open(truth_file, "r") as f:
        expected_hash = f.read().strip()

    with open(hash_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The bad commit hash in {hash_file} is incorrect. Expected '{expected_hash}', got '{actual_hash}'."