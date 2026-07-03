# test_final_state.py

import os
import re
import stat
import pytest

def test_analysis_txt_content():
    """Verify the contents of the analysis.txt file."""
    analysis_path = "/home/user/analysis.txt"
    assert os.path.isfile(analysis_path), f"File missing: {analysis_path}"

    with open(analysis_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) >= 2, f"{analysis_path} must contain at least two lines."
    assert lines[0] == "handle_client", f"Line 1 of {analysis_path} is incorrect. Expected 'handle_client'."
    assert lines[1] == "128", f"Line 2 of {analysis_path} is incorrect. Expected '128'."

def test_service_c_patched():
    """Verify that service.c has been patched with the seccomp sandbox logic."""
    service_c_path = "/home/user/src/service.c"
    assert os.path.isfile(service_c_path), f"File missing: {service_c_path}"

    with open(service_c_path, "r") as f:
        content = f.read()

    # Check for the apply_sandbox function definition
    assert "apply_sandbox" in content, "The function 'apply_sandbox' is missing in service.c."

    # Check if apply_sandbox is called inside main
    main_match = re.search(r'int\s+main\s*\([^)]*\)\s*\{([^}]+)', content)
    assert main_match is not None, "Could not find main() function in service.c."
    assert "apply_sandbox" in main_match.group(1), "apply_sandbox() is not called inside main()."

    # Check for seccomp and prctl related keywords
    assert "prctl" in content, "prctl system call is missing in service.c."
    assert "PR_SET_NO_NEW_PRIVS" in content, "PR_SET_NO_NEW_PRIVS is missing in service.c."

    # Check for seccomp filter installation
    has_seccomp = "SECCOMP_SET_MODE_FILTER" in content or "PR_SET_SECCOMP" in content or "seccomp_init" in content
    assert has_seccomp, "Seccomp filter installation logic is missing in service.c."

    # Check for execve/execveat syscall numbers or names
    has_execve = "59" in content or "SYS_execve" in content or "execve" in content
    has_execveat = "322" in content or "SYS_execveat" in content or "execveat" in content
    assert has_execve, "Filtering for execve (syscall 59) is missing in service.c."
    assert has_execveat, "Filtering for execveat (syscall 322) is missing in service.c."

def test_service_secured_binary_exists_and_executable():
    """Verify that the patched service is compiled and executable."""
    binary_path = "/home/user/service_secured"
    assert os.path.isfile(binary_path), f"Compiled binary missing: {binary_path}"

    # Check if the file is executable
    st = os.stat(binary_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"The file {binary_path} is not executable."