# test_final_state.py

import os
import re

def test_recovered_file_exists():
    """Test if the recovered.txt file was generated."""
    assert os.path.isfile("/home/user/recovered.txt"), "The file /home/user/recovered.txt was not generated."

def test_recovered_file_content():
    """Test if the recovered.txt file contains the correct final database state."""
    expected_content = (
        "admin user=john smith\n"
        "background task=running\n"
        "error log=disk full\n"
        "system_status=online\n"
    )

    with open("/home/user/recovered.txt", "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"The content of /home/user/recovered.txt is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{actual_content}"
    )

def test_executable_exists():
    """Test if the recover executable was compiled."""
    assert os.path.isfile("/home/user/recover"), "The executable /home/user/recover was not found."
    assert os.access("/home/user/recover", os.X_OK), "The file /home/user/recover is not executable."

def test_c_code_fixed():
    """Test if the C code was modified to fix the parsing bug and race condition."""
    assert os.path.isfile("/home/user/recover.c"), "The file /home/user/recover.c is missing."

    with open("/home/user/recover.c", "r") as f:
        content = f.read()

    # Check for mutex usage (lock and unlock)
    assert "pthread_mutex_lock" in content, "The C code does not appear to use pthread_mutex_lock to fix the race condition."
    assert "pthread_mutex_unlock" in content, "The C code does not appear to use pthread_mutex_unlock to fix the race condition."

    # Check for fixed parsing logic, typically sscanf with "%[^\"]" or similar logic instead of just "%s %s"
    assert "%s" not in content or "%[^" in content or "strtok" in content or "strchr" in content, (
        "The C code does not seem to have the fixed parsing logic for spaces."
    )