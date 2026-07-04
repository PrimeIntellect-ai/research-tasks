# test_final_state.py

import os
import re
import pytest

def test_bad_commit_hash():
    """Test that the bad commit hash was correctly identified and written."""
    expected_path = "/tmp/expected_bad_commit.txt"
    actual_path = "/home/user/bad_commit_hash.txt"

    assert os.path.isfile(actual_path), f"The file {actual_path} is missing."

    with open(expected_path, 'r') as f:
        expected_hash = f.read().strip()

    with open(actual_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, (
        f"Incorrect bad commit hash in {actual_path}. "
        f"Expected '{expected_hash}', got '{actual_hash}'."
    )

def test_fix_patch_contents():
    """Test that the patch file exists, is valid, and contains the correct fix."""
    patch_path = "/home/user/fix.patch"

    assert os.path.isfile(patch_path), f"The file {patch_path} is missing."

    with open(patch_path, 'r') as f:
        patch_content = f.read()

    # Verify it looks like a unified diff
    assert re.search(r'^--- ', patch_content, re.MULTILINE) and re.search(r'^\+\+\+ ', patch_content, re.MULTILINE), \
        f"The file {patch_path} does not appear to be a valid unified diff."

    # Verify the memory leak fix (addition of delete[] buffer;)
    fix_match = re.search(r'^\+\s*delete\s*\[\s*\]\s*buffer\s*;', patch_content, re.MULTILINE)
    assert fix_match is not None, (
        f"The patch in {patch_path} does not add the required 'delete[] buffer;' statement."
    )

    # Verify that the core logic was not removed
    removed_allocation = re.search(r'^-\s*char\s*\*\s*buffer\s*=\s*new\s*char\[1024\]\s*;', patch_content, re.MULTILINE)
    assert removed_allocation is None, (
        f"The patch in {patch_path} incorrectly removes the original buffer allocation logic."
    )