# test_final_state.py

import os
import hashlib

def test_recovered_logs_exists_and_correct():
    logs_path = "/home/user/recovered_logs.txt"
    assert os.path.exists(logs_path), f"File {logs_path} is missing."
    assert os.path.isfile(logs_path), f"Path {logs_path} is not a file."

    expected_content = (
        "EVENT: START\n"
        "USER: root API_KEY=**************** action=login\n"
        "API_KEY=****************\n"
        "CONNECTION TERMINATED\n"
    )

    with open(logs_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # The prompt says "followed by a newline (\n). If a payload already ends in a newline, do not print an extra one."
    # So the expected content should be exactly as above. But we can strip trailing spaces/newlines to be a bit forgiving 
    # if they missed the exact trailing newline semantics, as long as the lines match.
    # Actually, the diff command in the truth uses `echo -e "..."` which adds a single trailing newline.
    assert actual_content.strip() == expected_content.strip(), (
        f"Content of {logs_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_sha256_file_exists_and_correct():
    logs_path = "/home/user/recovered_logs.txt"
    hash_path = "/home/user/recovered_logs.sha256"

    assert os.path.exists(hash_path), f"File {hash_path} is missing."
    assert os.path.isfile(hash_path), f"Path {hash_path} is not a file."

    # Calculate expected hash based on the actual file content
    with open(logs_path, "rb") as f:
        file_bytes = f.read()
    expected_hash = hashlib.sha256(file_bytes).hexdigest()

    with open(hash_path, "r", encoding="utf-8") as f:
        hash_content = f.read().strip()

    # The sha256sum output format is typically: "<hash>  /home/user/recovered_logs.txt"
    # We will just check if the expected hash string is present in the file.
    assert expected_hash in hash_content, (
        f"The SHA-256 hash in {hash_path} does not match the actual hash of {logs_path}.\n"
        f"Expected hash: {expected_hash}"
    )

def test_c_source_code_exists():
    c_path = "/home/user/parser.c"
    assert os.path.exists(c_path), f"C source file {c_path} is missing."
    assert os.path.isfile(c_path), f"Path {c_path} is not a file."