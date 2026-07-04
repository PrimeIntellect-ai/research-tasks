# test_final_state.py

import os
import stat
import subprocess
import hashlib

def test_task_completion():
    token_file = "/home/user/new_token.txt"
    script_file = "/home/user/rotate_token.sh"

    # 1. Check if token file exists and has correct initial content
    assert os.path.exists(token_file), f"{token_file} does not exist. Did you execute your script to create it?"

    with open(token_file, "r") as f:
        content = f.read().strip()

    # The expected token based on the vulnerable log entry: port 8082, token tok_789ghi
    expected_initial_hash = hashlib.sha256(b"8082:tok_789ghi:secret_salt_2024").hexdigest()
    assert content == expected_initial_hash, f"Incorrect hash in {token_file}. Expected {expected_initial_hash}, got {content}. Make sure you identified the correct log entry and formatted the string correctly."

    # 2. Check script existence and executable permissions
    assert os.path.exists(script_file), f"{script_file} does not exist."
    st = os.stat(script_file)
    assert st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH), f"{script_file} is not executable."

    # 3. Check script functionality with dummy arguments to ensure it doesn't hardcode the output
    test_port = "9999"
    test_token = "tok_test123"
    expected_test_hash = hashlib.sha256(f"{test_port}:{test_token}:secret_salt_2024".encode()).hexdigest()

    try:
        result = subprocess.run([script_file, test_port, test_token], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"Script execution failed with return code {result.returncode}: {result.stderr}"
    except Exception as e:
        assert False, f"Failed to execute {script_file}: {e}"

    # Verify the script wrote the new correct hash to the file
    with open(token_file, "r") as f:
        new_content = f.read().strip()

    assert new_content == expected_test_hash, f"Script did not compute the correct hash for test arguments. Expected {expected_test_hash}, got {new_content}. Ensure it correctly uses the arguments passed to it."