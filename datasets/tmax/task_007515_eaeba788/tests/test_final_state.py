# test_final_state.py

import os
import stat
import pytest

def test_rust_project_exists():
    """Check if the Rust project directory exists."""
    dir_path = "/home/user/redactor"
    assert os.path.isdir(dir_path), f"Rust project directory {dir_path} does not exist."
    # Basic check for Cargo.toml to ensure it's a Rust project
    cargo_toml = os.path.join(dir_path, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {dir_path}. Is it a valid Rust project?"

def test_safe_log_exists():
    """Check if the sanitized log file was created."""
    file_path = "/home/user/incident_logs/app_trace_safe.log"
    assert os.path.isfile(file_path), f"Sanitized log file {file_path} does not exist."

def test_safe_log_permissions():
    """Check if the sanitized log file has exactly 0400 permissions."""
    file_path = "/home/user/incident_logs/app_trace_safe.log"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    file_stat = os.stat(file_path)
    # Extract the permission bits
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o400, f"Expected permissions 0o400 (read-only for owner), but got {oct(permissions)}."

def test_safe_log_content():
    """Check if the sanitized log file has the correctly redacted content."""
    file_path = "/home/user/incident_logs/app_trace_safe.log"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_content = (
        "[INFO] User logged in. SESSION_TOKEN=[REDACTED]\n"
        "[DEBUG] Connecting to DB. PASSWORD=[REDACTED]\n"
        "[INFO] Action executed by SESSION_TOKEN=[REDACTED]\n"
        "[ERROR] Failed auth. PASSWORD=[REDACTED]\n"
        "[INFO] Normal log entry without sensitive data."
    )

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, "The content of the sanitized log does not match the expected redacted output."