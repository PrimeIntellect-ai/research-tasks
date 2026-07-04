# test_final_state.py

import os
import pytest

def compute_checksum(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return sum(data) % 256

def get_expected_manifest_lines(target_dir):
    lines = []
    # os.walk follows symlinks if followlinks=True, default is False.
    # However, we should manually skip symlinked directories just in case.
    for root, dirs, files in os.walk(target_dir):
        # Remove symlinked dirs to avoid traversing them
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

        for name in files:
            filepath = os.path.join(root, name)
            if not os.path.islink(filepath) and os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                checksum = compute_checksum(filepath)
                lines.append(f"{filepath} {size} {checksum}")
    lines.sort()
    return lines

def test_tracker_cpp_exists():
    assert os.path.isfile("/home/user/tracker.cpp"), "/home/user/tracker.cpp is missing. Did you write the C++ program?"

def test_manifest_exists():
    assert os.path.isfile("/home/user/manifest.txt"), "/home/user/manifest.txt is missing. Did the program run successfully?"

def test_manifest_contents():
    target_dir = "/home/user/config_data"
    manifest_path = "/home/user/manifest.txt"

    assert os.path.isdir(target_dir), f"Target directory {target_dir} is missing."
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    expected_lines = get_expected_manifest_lines(target_dir)

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Manifest contents do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )