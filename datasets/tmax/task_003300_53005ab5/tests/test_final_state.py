# test_final_state.py
import os
import pytest

def test_update_log_contents():
    """Verify the log file exists and contains exactly the expected safe paths."""
    log_path = '/home/user/update_log.txt'
    assert os.path.exists(log_path), f"Log file {log_path} was not created."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_paths = {
        '/home/user/docs/valid1.md',
        '/home/user/docs/subdir/valid2.md'
    }

    assert set(lines) == expected_paths, f"Log file contents incorrect. Expected {expected_paths}, got {set(lines)}."
    assert len(lines) == 2, "Log file should contain exactly two lines for the two safely extracted files."

def test_script_uses_locking():
    """Verify the script contains the required locking mechanisms."""
    script_path = '/home/user/process_updates.py'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'fcntl.flock' in content, "Script does not appear to use fcntl.flock for concurrent-safe logging."
    assert 'fcntl.LOCK_EX' in content, "Script does not appear to use fcntl.LOCK_EX for exclusive locking."

def test_valid1_content():
    """Verify valid1.md was extracted and correctly tagged."""
    path = '/home/user/docs/valid1.md'
    assert os.path.exists(path), f"File {path} was not extracted."

    with open(path, 'r') as f:
        content = f.read()

    assert content.startswith("<!-- REVIEWED -->\n"), f"{path} does not start with the required REVIEWED tag."
    assert "Content of valid1" in content, f"{path} original content is missing or corrupted."

def test_valid2_content():
    """Verify valid2.md was extracted and correctly tagged."""
    path = '/home/user/docs/subdir/valid2.md'
    assert os.path.exists(path), f"File {path} was not extracted."

    with open(path, 'r') as f:
        content = f.read()

    assert content.startswith("<!-- REVIEWED -->\n"), f"{path} does not start with the required REVIEWED tag."
    assert "Content of valid2" in content, f"{path} original content is missing or corrupted."

def test_old_doc_unchanged():
    """Verify that older, existing documentation was not tagged."""
    path = '/home/user/docs/existing/old_doc.md'
    assert os.path.exists(path), f"Existing file {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    assert "<!-- REVIEWED -->" not in content, f"Old documentation at {path} should not have been tagged."
    assert "Old Documentation\nLine 2" in content, f"Original content of {path} was altered."

def test_path_traversal_prevented():
    """Verify that malicious path traversal payloads were successfully skipped."""
    bad_paths = [
        '/home/user/escaped.md',
        '/home/user/docs/escaped.md',
        '/home/user/absolute.md'
    ]

    for bad_path in bad_paths:
        assert not os.path.exists(bad_path), f"Path traversal vulnerability detected! Malicious file {bad_path} was extracted."