# test_final_state.py

import os
import re
import pytest

def test_minimal_trigger_file_exists():
    path = "/home/user/minimal_trigger.txt"
    assert os.path.isfile(path), f"File {path} does not exist. You must create it with the minimal trigger."

def test_minimal_trigger_content():
    path = "/home/user/minimal_trigger.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # The instructions say: "must contain ONLY the hexadecimal string and no other text or newlines"
    assert content == "deadbeef42", f"The content of {path} is incorrect. Expected 'deadbeef42', got {repr(content)}"

def test_c2_agent_build_failure_fixed():
    path = "/home/user/c2_agent/src/main.rs"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check if the build failure was fixed by importing std::io::Read
    # It should not be commented out.
    lines = content.splitlines()
    read_imported = any(re.search(r'^\s*use\s+std::io::Read\s*;', line) for line in lines)

    # Alternatively, they might have changed `file.read_to_end` to `std::io::Read::read_to_end(&mut file, ...)`
    # but fixing the import is the standard way. Let's just check if `std::io::Read` is used.
    assert "std::io::Read" in content, "The compilation error in main.rs does not appear to be fixed (std::io::Read is missing)."

    # Ensure it's not just the commented out version
    uncommented_read = any("std::io::Read" in line and not line.strip().startswith("//") for line in lines)
    assert uncommented_read, "The std::io::Read import is still commented out in main.rs."