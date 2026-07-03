# test_final_state.py
import os
import hashlib

def test_submission_file_exists():
    assert os.path.exists('/home/user/submission.txt'), "The file /home/user/submission.txt does not exist."

def test_submission_content():
    flag_path = '/home/user/flag.txt'
    assert os.path.exists(flag_path), f"The flag file {flag_path} is missing."

    # Read the exact content of the flag file
    with open(flag_path, 'rb') as f:
        flag_content = f.read()

    # Calculate the expected MD5 hash
    expected_hash = hashlib.md5(flag_content).hexdigest().lower()

    # Read the submission file
    with open('/home/user/submission.txt', 'r') as f:
        submission_content = f.read().strip().lower()

    assert expected_hash in submission_content, (
        f"The submission file does not contain the correct MD5 hash. "
        f"Expected to find '{expected_hash}' but got '{submission_content}'."
    )