# test_final_state.py

import os
import stat
import pytest

def test_filter_c_exists():
    """Check if the filter.c source file exists."""
    path = "/home/user/filter.c"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_filter_executable_exists():
    """Check if the compiled filter executable exists and is executable."""
    path = "/home/user/filter"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_verified_artifacts_log_exists_and_correct():
    """Check if the verified_artifacts.log exists and contains the correct output."""
    path = "/home/user/verified_artifacts.log"
    assert os.path.exists(path), f"Log file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    expected_lines = [
        "lib/math.obj",
        "include/math.h",
        "docs/readme.txt"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {path} do not match the expected output. "
        f"Expected: {expected_lines}, Got: {actual_lines}"
    )

def test_archive_not_extracted():
    """Ensure the archive was not extracted."""
    unexpected_paths = [
        "/home/user/lib",
        "/home/user/include",
        "/home/user/docs",
        "/home/user/artifacts/lib",
        "/home/user/artifacts/include",
        "/home/user/artifacts/docs"
    ]
    for path in unexpected_paths:
        assert not os.path.exists(path), f"Archive appears to be extracted; found {path}."