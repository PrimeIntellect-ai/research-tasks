# test_final_state.py

import os
import pytest

def test_restore_results_log_exists():
    """Test that the restore_results.log file was created."""
    filepath = "/home/user/restore_results.log"
    assert os.path.isfile(filepath), f"Expected file {filepath} to exist after running the startup sequence."

def test_restore_results_log_content():
    """Test that the restore_results.log contains the exact success message."""
    filepath = "/home/user/restore_results.log"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected = "RESTORE_SUCCESS: Verified data connection"
    assert content == expected, f"Content of {filepath} was '{content}', expected '{expected}'."

def test_rust_binary_compiled():
    """Test that the Rust application was compiled in release mode."""
    filepath = "/home/user/stack_restore/app/target/release/restore_verifier"
    assert os.path.isfile(filepath), f"Compiled binary {filepath} is missing. Did you run 'cargo build --release'?"
    assert os.access(filepath, os.X_OK), f"File {filepath} is not executable."

def test_rust_code_modified():
    """Test that the Rust application source code was modified to use BACKEND_PORT."""
    filepath = "/home/user/stack_restore/app/src/main.rs"
    assert os.path.isfile(filepath), f"Source file {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    assert "BACKEND_PORT" in content, "The Rust source code does not appear to read the BACKEND_PORT environment variable."

def test_start_script_modified():
    """Test that start_all.sh was modified to include the port and export it."""
    filepath = "/home/user/stack_restore/start_all.sh"
    assert os.path.isfile(filepath), f"Script {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    assert "8085" in content, "The start_all.sh script does not seem to contain the required port 8085."
    assert "BACKEND_PORT" in content, "The start_all.sh script does not seem to export or set the BACKEND_PORT environment variable."