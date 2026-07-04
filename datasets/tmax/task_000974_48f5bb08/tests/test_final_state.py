# test_final_state.py
import os
import re

def test_recovered_docs_directory_exists():
    """Verify that the recovered_docs directory was created."""
    assert os.path.isdir('/home/user/recovered_docs'), "Directory /home/user/recovered_docs does not exist."

def test_recovered_files_exist_and_correct():
    """Verify that the valid files were extracted correctly."""
    base_dir = '/home/user/recovered_docs'

    expected_files = {
        'index.md': b'# Index\nWelcome to docs.',
        'api/v1.md': b'# API v1\nSpecs here.',
        'shared/styles.css': b'body { color: black; }'
    }

    for rel_path, expected_content in expected_files.items():
        full_path = os.path.join(base_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected file {full_path} is missing."
        with open(full_path, 'rb') as f:
            content = f.read()
        assert content == expected_content, f"Content of {full_path} does not match expected."

def test_infinite_loop_avoided():
    """Verify that files with 'shared/shared/' were NOT extracted."""
    bad_path = '/home/user/recovered_docs/shared/shared'
    assert not os.path.exists(bad_path), f"Found {bad_path}, which means the infinite loop was not correctly stopped."

def test_recovery_log_content():
    """Verify the contents of the recovery.log file."""
    log_path = '/home/user/recovery.log'
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    expected_log = (
        "index.md: 23 bytes\n"
        "api/v1.md: 20 bytes\n"
        "shared/styles.css: 22 bytes\n"
    )

    with open(log_path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_log.strip(), f"Content of {log_path} is incorrect."

def test_posix_locking_used():
    """Verify that POSIX file locking was used in the C++ source code."""
    cpp_path = '/home/user/recover.cpp'
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, 'r') as f:
        code = f.read()

    has_flock = re.search(r'\bflock\s*\(', code) and re.search(r'\bLOCK_EX\b', code)
    has_fcntl = re.search(r'\bfcntl\s*\(', code) and re.search(r'\bF_WRLCK\b', code)

    assert has_flock or has_fcntl, "Could not find POSIX file locking (flock with LOCK_EX or fcntl with F_WRLCK) in recover.cpp."