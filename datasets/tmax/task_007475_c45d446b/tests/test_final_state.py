# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    assert os.path.isfile("/home/user/checksum_gen.cpp"), "C++ source file /home/user/checksum_gen.cpp is missing."

def test_cpp_executable_exists():
    assert os.path.isfile("/home/user/checksum_gen"), "Compiled executable /home/user/checksum_gen is missing."
    assert os.access("/home/user/checksum_gen", os.X_OK), "/home/user/checksum_gen is not executable."

def test_bash_script_exists():
    assert os.path.isfile("/home/user/backup.sh"), "Bash script /home/user/backup.sh is missing."

def test_backup_manifest_correctness():
    manifest_path = "/home/user/backup_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing. Did you run backup.sh?"

    log_dir = "/home/user/active_logs"
    expected_lines = []

    # Recompute expected state dynamically based on the rules
    for root, _, files in os.walk(log_dir):
        for file in files:
            if file.endswith(".log"):
                filepath = os.path.join(root, file)
                if os.path.getsize(filepath) > 10:
                    with open(filepath, "rb") as f:
                        data = f.read()
                    checksum = sum(data) % 256
                    expected_lines.append(f"{filepath} {checksum}\n")

    expected_lines.sort()

    with open(manifest_path, "r") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, (
        f"Manifest contents are incorrect.\n"
        f"Expected:\n{''.join(expected_lines)}\n"
        f"Got:\n{''.join(actual_lines)}"
    )