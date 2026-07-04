# test_final_state.py

import os
import pytest

def test_clean_system_log_exists_and_content():
    """Verify that the clean system log exists and has the correct UTF-8 content."""
    clean_log_file = "/home/user/staging/clean_system.log"

    assert os.path.exists(clean_log_file), f"File {clean_log_file} does not exist. Did the Rust program run successfully?"
    assert os.path.isfile(clean_log_file), f"{clean_log_file} is not a file."

    expected_content = (
        "LOG ENTRY 1: System started\n"
        "LOG ENTRY 2: User login [REDACTED]\n"
        "LOG ENTRY 3: Résumé processed for [REDACTED]\n"
        "LOG ENTRY 4: System shutdown\n"
    )

    # Read as bytes first to ensure it's valid UTF-8
    with open(clean_log_file, "rb") as f:
        raw_content = f.read()

    try:
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"The file {clean_log_file} is not valid UTF-8.")

    assert "[SECRET_ID]" not in content, "The string [SECRET_ID] was not completely redacted."
    assert "[REDACTED]" in content, "The string [REDACTED] was not found in the output."
    assert "Résumé" in content, "The ISO-8859-1 characters were not correctly converted to UTF-8."

    assert content == expected_content, f"Content of {clean_log_file} does not match the expected output."

def test_rust_program_uses_atomic_rename():
    """Verify that the Rust program exists and uses atomic rename."""
    rust_file = "/home/user/process_log.rs"

    assert os.path.exists(rust_file), f"Rust source file {rust_file} does not exist."
    assert os.path.isfile(rust_file), f"{rust_file} is not a file."

    with open(rust_file, "r", encoding="utf-8", errors="ignore") as f:
        source_code = f.read()

    assert "rename" in source_code, "The Rust program does not appear to use an atomic rename operation (e.g., std::fs::rename)."