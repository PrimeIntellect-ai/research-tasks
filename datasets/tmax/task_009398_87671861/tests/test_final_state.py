# test_final_state.py

import os
import re
import pytest

def test_c_program_exists_and_uses_locks():
    c_file = "/home/user/rle_processor.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing"

    with open(c_file, "r") as f:
        content = f.read()

    has_flock = "flock" in content and "LOCK_EX" in content
    has_fcntl = "fcntl" in content and "F_WRLCK" in content # or F_SETLKW
    has_fcntl_fallback = "fcntl" in content and "F_SETLKW" in content

    assert has_flock or has_fcntl or has_fcntl_fallback, "C program must use flock() or fcntl() for exclusive file locking"

def test_compiled_program_exists():
    bin_file = "/home/user/rle_processor"
    assert os.path.isfile(bin_file), f"Compiled binary {bin_file} is missing"
    assert os.access(bin_file, os.X_OK), f"Compiled binary {bin_file} is not executable"

def test_master_doc_content():
    out_file = "/home/user/master_doc.txt"
    assert os.path.isfile(out_file), f"Output file {out_file} is missing"

    with open(out_file, "r") as f:
        content = f.read().strip()

    assert content in ["TTesstMaster", "MasterTTesst"], f"Content of {out_file} is incorrect. Expected 'TTesstMaster' or 'MasterTTesst', got '{content}'"
    assert "FAIL" not in content, f"Content of {out_file} contains data from the ignored old file"