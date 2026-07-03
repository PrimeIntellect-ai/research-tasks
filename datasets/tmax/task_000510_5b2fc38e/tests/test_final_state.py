# test_final_state.py

import os
import itertools
import pytest

def get_expected_bypasses():
    # Generate all case permutations of "admin"
    perms = [''.join(p) for p in itertools.product(*zip('admin', 'ADMIN'))]
    # "admin" is already in the original config, so it should be blocked and not bypassed
    perms.remove('admin')
    return sorted(perms)

def test_bypasses_log():
    log_path = '/home/user/bypasses.log'
    assert os.path.exists(log_path), f"File not found: {log_path}"

    with open(log_path, 'r') as f:
        actual_lines = f.read().splitlines()

    expected_bypasses = get_expected_bypasses()
    assert actual_lines == expected_bypasses, (
        f"{log_path} does not contain the correct sorted bypassing permutations. "
        f"Expected {len(expected_bypasses)} items, got {len(actual_lines)}."
    )

def test_config_txt_orig():
    orig_path = '/home/user/config.txt.orig'
    assert os.path.exists(orig_path), f"Backup file not found: {orig_path}"

    with open(orig_path, 'r') as f:
        actual_lines = f.read().splitlines()

    expected_original = ['root', 'admin', 'superuser']
    assert actual_lines == expected_original, (
        f"{orig_path} does not contain the expected original configuration."
    )

def test_config_txt_updated():
    config_path = '/home/user/config.txt'
    assert os.path.exists(config_path), f"File not found: {config_path}"

    with open(config_path, 'r') as f:
        actual_lines = f.read().splitlines()

    expected_original = ['root', 'admin', 'superuser']
    assert actual_lines[:3] == expected_original, (
        f"The first 3 lines of {config_path} must remain the original configuration."
    )

    added_lines = actual_lines[3:]
    expected_bypasses = get_expected_bypasses()

    # The instructions say "Append all discovered bypassing permutations to /home/user/config.txt"
    # We will verify that exactly the expected bypasses were added, ignoring order for this specific check
    # though they should ideally be sorted if appended from the log.
    assert sorted(added_lines) == sorted(expected_bypasses), (
        f"{config_path} does not have the correct bypassing permutations appended."
    )

def test_config_patch():
    patch_path = '/home/user/config.patch'
    assert os.path.exists(patch_path), f"Patch file not found: {patch_path}"

    with open(patch_path, 'r') as f:
        patch_content = f.read()

    # Check for unified diff headers
    assert "---" in patch_content and "+++" in patch_content, (
        f"{patch_path} does not appear to be a unified diff."
    )

    assert "/home/user/config.txt.orig" in patch_content or "config.txt.orig" in patch_content, (
        f"{patch_path} does not reference the original file config.txt.orig."
    )

    assert "/home/user/config.txt" in patch_content or "config.txt" in patch_content, (
        f"{patch_path} does not reference the modified file config.txt."
    )

    expected_bypasses = get_expected_bypasses()
    patch_lines = patch_content.splitlines()

    # Extract added lines from the patch
    added_in_patch = [
        line[1:] for line in patch_lines 
        if line.startswith('+') and not line.startswith('+++')
    ]

    for p in expected_bypasses:
        assert p in added_in_patch, f"Patch is missing the addition of bypass: {p}"