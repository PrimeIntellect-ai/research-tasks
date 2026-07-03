# test_final_state.py

import os
import stat

def test_c_source_code_exists():
    """Verify that the C source code file exists."""
    src_path = "/home/user/get_restore_chain.c"
    assert os.path.exists(src_path), f"C source file {src_path} does not exist."
    assert os.path.isfile(src_path), f"Path {src_path} is not a file."

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_path = "/home/user/get_restore_chain"
    assert os.path.exists(exe_path), f"Compiled executable {exe_path} does not exist."
    assert os.path.isfile(exe_path), f"Path {exe_path} is not a file."

    # Check if the file is executable
    st = os.stat(exe_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {exe_path} is not executable."

def test_restore_plan_csv_content():
    """Verify that the restore plan CSV was created and contains the correct shortest path."""
    csv_path = "/home/user/restore_plan.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file."

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected_content = "full_base_001,shortcut_diff,incr_log_999"
    assert content == expected_content, (
        f"Incorrect path found in {csv_path}.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual:   '{content}'"
    )