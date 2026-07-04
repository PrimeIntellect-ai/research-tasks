# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/workspace"
RUST_LIB = os.path.join(WORKSPACE_DIR, "rust_part", "target", "release", "librust_part.so")
C_LIB = os.path.join(WORKSPACE_DIR, "c_part", "libcchecksum.so")
PYTHON_SCRIPT = os.path.join(WORKSPACE_DIR, "verify_token.py")
LOG_FILE = os.path.join(WORKSPACE_DIR, "build_artifacts.log")

def test_rust_lib_built():
    assert os.path.isfile(RUST_LIB), f"Rust shared library not found at {RUST_LIB}. Did 'cargo build --release' succeed?"

def test_c_lib_built():
    assert os.path.isfile(C_LIB), f"C shared library not found at {C_LIB}. Did the Makefile compile it correctly?"

def test_python_script_exists():
    assert os.path.isfile(PYTHON_SCRIPT), f"Python script not found at {PYTHON_SCRIPT}."

def test_log_file_content():
    assert os.path.isfile(LOG_FILE), f"Log file not found at {LOG_FILE}."

    with open(LOG_FILE, "r") as f:
        content = f.read().strip()

    expected_content = "Rust Checksum: 1946\nC Checksum: 2552695574"

    assert content == expected_content, f"Log file content does not match expected.\nExpected:\n{expected_content}\n\nGot:\n{content}"