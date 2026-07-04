# test_final_state.py
import os

def test_bad_commit_hash():
    bad_commit_file = "/home/user/bad_commit.txt"
    hidden_file = "/tmp/.hidden_bad_commit"

    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist. Did you save the bad commit hash?"
    assert os.path.isfile(hidden_file), f"Setup error: {hidden_file} does not exist."

    with open(bad_commit_file, "r") as f:
        student_hash = f.read().strip()

    with open(hidden_file, "r") as f:
        truth_hash = f.read().strip()

    assert student_hash == truth_hash, f"Commit hash in {bad_commit_file} is incorrect. Expected {truth_hash}, got {student_hash}."

def test_fixed_output():
    output_file = "/home/user/fixed_output.txt"

    assert os.path.isfile(output_file), f"{output_file} does not exist. Did you run the fixed executable and redirect output?"

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_content = "SYSTEM_START_OK_\nUSER_AUTH_SUCCES\nDB_CONNECT_READY"

    assert content == expected_content, f"The output in {output_file} does not match the expected decoded text. Got:\n{content}"