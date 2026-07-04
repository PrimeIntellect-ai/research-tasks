# test_final_state.py

import os
import pytest

def test_snapshot_log_exists():
    assert os.path.isfile("/home/user/snapshot.log"), "/home/user/snapshot.log does not exist."

def test_snapshot_tmp_does_not_exist():
    assert not os.path.exists("/home/user/snapshot.tmp"), "/home/user/snapshot.tmp should not exist (must be atomically renamed)."

def test_snapshot_log_content():
    configs_dir = "/home/user/configs"
    conf_files = []

    # Recursively find all .conf files
    for root, _, files in os.walk(configs_dir):
        for file in files:
            if file.endswith(".conf"):
                conf_files.append(os.path.join(root, file))

    # Sort lexicographically by absolute path
    conf_files.sort()

    expected_content = ""
    for conf_file in conf_files:
        with open(conf_file, "r") as f:
            content = f.read()

        expected_content += f"FILE: {conf_file}\n"
        expected_content += "CONTENT:\n"
        expected_content += content
        if not expected_content.endswith("\n"):
            expected_content += "\n"
        expected_content += "EOF\n"

    with open("/home/user/snapshot.log", "r") as f:
        actual_content = f.read()

    # Standardize newlines for comparison
    actual_content = actual_content.strip() + "\n"
    expected_content = expected_content.strip() + "\n"

    assert actual_content == expected_content, "The contents of /home/user/snapshot.log do not match the expected format and data."

def test_c_source_code_requirements():
    source_file = "/home/user/config_snapshot.c"
    assert os.path.isfile(source_file), f"Source file {source_file} is missing."

    with open(source_file, "r") as f:
        source_code = f.read()

    assert "mmap" in source_code, "The C program must use 'mmap' for memory-mapped I/O."
    assert "flock" in source_code or "fcntl" in source_code, "The C program must use 'flock' or 'fcntl' for file locking."
    assert "rename" in source_code, "The C program must use 'rename' for atomic file replacement."