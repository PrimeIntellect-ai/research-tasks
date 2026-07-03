# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/websec_project"

def test_directories_exist():
    """Verify that the required directories have been created."""
    expected_dirs = ["src", "include", "lib", "tests"]
    for d in expected_dirs:
        dir_path = os.path.join(PROJECT_DIR, d)
        assert os.path.isdir(dir_path), f"Expected directory {dir_path} does not exist."

def test_file_relocations():
    """Verify that the source files were moved to their correct directories."""
    checksum_c = os.path.join(PROJECT_DIR, "src", "checksum.c")
    checksum_h = os.path.join(PROJECT_DIR, "include", "checksum.h")

    assert os.path.isfile(checksum_c), f"File {checksum_c} is missing. Was it moved?"
    assert os.path.isfile(checksum_h), f"File {checksum_h} is missing. Was it moved?"

    # Also verify they are no longer in the root
    assert not os.path.exists(os.path.join(PROJECT_DIR, "checksum.c")), "checksum.c should not be in the project root."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "checksum.h")), "checksum.h should not be in the project root."

def test_shared_library_abi():
    """Verify the shared library exists and has the correct exported/hidden symbols."""
    lib_path = os.path.join(PROJECT_DIR, "lib", "libwebsec.so")
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist."

    # Run nm -D to check dynamic symbols
    result = subprocess.run(["nm", "-D", lib_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run nm on {lib_path}. Is it a valid shared object?"

    output = result.stdout

    # generate_web_token_hash MUST be exported (T or similar)
    assert "generate_web_token_hash" in output, "Symbol 'generate_web_token_hash' is missing from the dynamic symbol table."

    # internal_mix_entropy MUST NOT be exported
    assert "internal_mix_entropy" not in output, "Symbol 'internal_mix_entropy' is exported in the dynamic symbol table, but it MUST be hidden."

def test_executable_and_log():
    """Verify the test executable exists, is executable, and the log has the correct output."""
    exe_path = os.path.join(PROJECT_DIR, "tests", "prop_test")
    log_path = os.path.join(PROJECT_DIR, "test_result.log")

    assert os.path.isfile(exe_path), f"Test executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "PROPERTY_TEST_SUCCESS", f"Log file content is incorrect. Expected 'PROPERTY_TEST_SUCCESS', got '{content}'."