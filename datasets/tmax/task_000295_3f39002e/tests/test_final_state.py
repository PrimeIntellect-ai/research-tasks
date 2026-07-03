# test_final_state.py

import os
import pytest

def test_migration_log_exists_and_content():
    """Verify that migration.log exists and contains the correct sorted paths."""
    log_path = "/home/user/migration.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/workspace/docs/file1.md",
        "/home/user/workspace/docs/sub/file3.md"
    ]
    assert lines == expected_lines, f"migration.log contents incorrect. Expected {expected_lines}, got {lines}"

def test_modified_files():
    """Verify that the targeted files were properly modified."""
    file1 = "/home/user/workspace/docs/file1.md"
    file3 = "/home/user/workspace/docs/sub/file3.md"

    for file_path in [file1, file3]:
        assert os.path.isfile(file_path), f"Expected file not found: {file_path}"
        with open(file_path, "r") as f:
            content = f.read()

        assert "[UPDATED_MACRO]" in content, f"{file_path} missing [UPDATED_MACRO]"
        assert "NewCorp" in content, f"{file_path} missing NewCorp"
        assert "[DEPRECATED_MACRO]" not in content, f"{file_path} still contains [DEPRECATED_MACRO]"
        assert "OldCorp" not in content, f"{file_path} still contains OldCorp"

def test_unmodified_files():
    """Verify that files not meeting the criteria were NOT modified."""
    file2 = "/home/user/workspace/docs/file2.md"
    file4 = "/home/user/workspace/docs/file4.txt"

    assert os.path.isfile(file2), f"Expected file not found: {file2}"
    with open(file2, "r") as f:
        content2 = f.read()

    assert "OldCorp" in content2, f"{file2} should still contain OldCorp"
    assert "NewCorp" not in content2, f"{file2} should not contain NewCorp"

    assert os.path.isfile(file4), f"Expected file not found: {file4}"
    with open(file4, "r") as f:
        content4 = f.read()

    assert "[DEPRECATED_MACRO]" in content4, f"{file4} should still contain [DEPRECATED_MACRO]"
    assert "OldCorp" in content4, f"{file4} should still contain OldCorp"
    assert "[UPDATED_MACRO]" not in content4, f"{file4} should not contain [UPDATED_MACRO]"
    assert "NewCorp" not in content4, f"{file4} should not contain NewCorp"