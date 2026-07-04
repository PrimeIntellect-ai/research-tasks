# test_final_state.py

import os
import re
import pytest

def compute_dir_size_like_rust(path):
    total_size = 0
    try:
        for entry in os.scandir(path):
            stat = entry.stat(follow_symlinks=False)
            # In the Rust code, if it's a directory (and we don't follow symlinks), we recurse
            # is_dir() in Rust with symlink_metadata returns false for symlinks.
            if stat.st_mode & 0o170000 == 0o040000:  # Directory
                total_size += compute_dir_size_like_rust(entry.path)
            else:
                total_size += stat.st_size
    except Exception:
        pass
    return total_size

def test_rust_code_fixed():
    main_rs = "/home/user/scanner/src/main.rs"
    assert os.path.isfile(main_rs), f"Rust source file missing: {main_rs}"

    with open(main_rs, "r") as f:
        content = f.read()

    # The student should have replaced fs::metadata with fs::symlink_metadata
    # or implemented another way to avoid following symlinks.
    # A simple check is that they are no longer just blindly using fs::metadata
    # without checking for symlinks. We will check if symlink_metadata is used.
    assert "symlink_metadata" in content, "The Rust code does not appear to use 'symlink_metadata' to fix the symlink loop."

def test_executable_built():
    exe_path = "/home/user/scanner/target/release/scanner"
    assert os.path.isfile(exe_path), f"Compiled executable missing: {exe_path}. Did you run 'cargo build --release'?"
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_final_sizes_output():
    output_file = "/home/user/final_sizes.txt"
    assert os.path.isfile(output_file), f"Output file missing: {output_file}"

    with open(output_file, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # Parse config to get expected directories
    config_path = "/home/user/backup_config.conf"
    expected_dirs = []
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SCAN_DIR="):
                    expected_dirs.append(line.split("=", 1)[1])

    assert expected_dirs, "Could not find any SCAN_DIR entries in the config file."

    # Compute expected sizes
    expected_results = {}
    for d in expected_dirs:
        expected_results[d] = compute_dir_size_like_rust(d)

    # Check that all expected directories are in the output with the correct size
    for d, expected_size in expected_results.items():
        expected_line = f"{d} - Total size: {expected_size} bytes"
        assert expected_line in lines, f"Expected output line not found: '{expected_line}'. Actual output:\n{content}"

    assert len(lines) == len(expected_dirs), f"Output file has {len(lines)} lines, but expected {len(expected_dirs)}."