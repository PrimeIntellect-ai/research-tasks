# test_final_state.py

import os
import stat

def test_rust_source_exists():
    source_file = "/home/user/spectral_profiler.rs"
    assert os.path.isfile(source_file), f"Rust source file missing: {source_file}"

def test_executable_exists_and_runnable():
    executable = "/home/user/spectral_profiler"
    assert os.path.isfile(executable), f"Compiled executable missing: {executable}"

    # Check if it is executable
    st = os.stat(executable)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File is not executable: {executable}"

def test_mesh_validation_log_content():
    log_file = "/home/user/mesh_validation.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    expected_lines = [
        "Mesh 0: 18.0 - INVALID",
        "Mesh 1: 30.5 - INVALID",
        "Mesh 2: 43.0 - VALID",
        "Mesh 3: 55.5 - VALID"
    ]

    with open(log_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_file}, found {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"