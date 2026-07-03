# test_final_state.py

import os
import pytest

def test_pwned_log_exists():
    path = "/home/user/pwned.log"
    assert os.path.isfile(path), f"File {path} does not exist. The path traversal exploit was not successful or wrote to the wrong location."

def test_pwned_log_is_elf():
    path = "/home/user/pwned.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Check for ELF magic bytes
    with open(path, "rb") as f:
        magic = f.read(4)

    assert magic == b"\x7fELF", f"File {path} is not a valid ELF file. Expected magic bytes \\x7fELF, got {magic!r}."