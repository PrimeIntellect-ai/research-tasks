# test_final_state.py
import os

def test_bad_commit_hash_correct():
    result_path = '/home/user/bad_commit.txt'
    truth_path = '/tmp/ground_truth_bad_commit.txt'

    assert os.path.isfile(result_path), f"File {result_path} does not exist. The task requires writing the bad commit hash to this file."
    assert os.path.isfile(truth_path), f"Ground truth file {truth_path} does not exist."

    with open(result_path, 'r') as f:
        student_hash = f.read().strip()

    with open(truth_path, 'r') as f:
        truth_hash = f.read().strip()

    assert len(student_hash) == 40, f"The commit hash in {result_path} must be exactly 40 characters long. Found: {student_hash}"
    assert student_hash == truth_hash, f"The commit hash in {result_path} is incorrect. Expected {truth_hash}, but got {student_hash}."