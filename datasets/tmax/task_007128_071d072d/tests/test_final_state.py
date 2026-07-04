# test_final_state.py

import os
import stat
import subprocess
import hashlib
import pytest

def test_malicious_files_log():
    log_path = "/home/user/malicious_files.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    # Compute expected files and hashes
    expected_lines = []
    base_dir = "/home/user"
    exclude_dir = "/home/user/data"

    for root, dirs, files in os.walk(base_dir):
        if root.startswith(exclude_dir):
            continue
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                with open(filepath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                expected_lines.append(f"{file_hash}  {filepath}")

    expected_lines.sort()

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, "The contents of malicious_files.log do not match the expected sorted sha256sum output."

def test_binary_exists_and_permissions():
    binary_path = "/home/user/processor_secure"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."

    st = os.stat(binary_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o750, f"Permissions for {binary_path} are {oct(permissions)}, expected 0o750."

def test_binary_blocks_traversal_dotdot():
    binary_path = "/home/user/processor_secure"
    target_file = "/home/user/test_traversal.txt"

    if os.path.exists(target_file):
        os.remove(target_file)

    result = subprocess.run(
        [binary_path, "../test_traversal.txt", "malicious_content"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, f"Expected exit code 1 for path traversal attempt, got {result.returncode}."
    assert result.stderr == "Invalid filename\n", f"Expected stderr 'Invalid filename\\n', got {repr(result.stderr)}."
    assert not os.path.exists(target_file), "The binary wrote the file despite the path traversal attempt."

def test_binary_blocks_traversal_slash():
    binary_path = "/home/user/processor_secure"

    result = subprocess.run(
        [binary_path, "sub/dir.txt", "malicious_content"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, f"Expected exit code 1 for path containing '/', got {result.returncode}."
    assert result.stderr == "Invalid filename\n", f"Expected stderr 'Invalid filename\\n', got {repr(result.stderr)}."

def test_binary_allows_safe():
    binary_path = "/home/user/processor_secure"
    safe_target = "/home/user/data/safe_test_file.txt"

    if os.path.exists(safe_target):
        os.remove(safe_target)

    result = subprocess.run(
        [binary_path, "safe_test_file.txt", "safe_content"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Expected exit code 0 for safe filename, got {result.returncode}."
    assert os.path.isfile(safe_target), "The binary did not create the safe file."

    with open(safe_target, "r") as f:
        content = f.read()

    assert content == "safe_content", "The binary did not write the correct content to the safe file."