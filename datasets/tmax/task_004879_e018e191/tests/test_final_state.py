# test_final_state.py

import os
import hashlib

def test_solution_file_exists():
    path = "/home/user/solution.txt"
    assert os.path.exists(path), f"The file {path} does not exist. Did you save your solution?"
    assert os.path.isfile(path), f"The path {path} exists but is not a regular file."

def test_solution_content():
    path = "/home/user/solution.txt"
    assert os.path.exists(path), f"Cannot verify content: {path} is missing."

    # Recompute the expected hash from the known flag to ensure fidelity
    expected_flag = "FLAG{jwt_alg_none_1s_d4ng3r0us_9921}"
    expected_hash = hashlib.sha256(expected_flag.encode('utf-8')).hexdigest()

    with open(path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content != "", f"The file {path} is empty."
    assert actual_content == expected_hash, (
        f"The content of {path} does not match the expected SHA-256 hash of the flag. "
        f"Ensure you extracted the correct flag and hashed it without trailing newlines."
    )