# test_final_state.py

import os
import pytest

def test_line_number_file():
    file_path = "/home/user/line_number.txt"
    assert os.path.isfile(file_path), f"Required output file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "734", f"Expected line number 734 in {file_path}, but found '{content}'."

def test_bug_report_file():
    file_path = "/home/user/bug_report.txt"
    assert os.path.isfile(file_path), f"Required output file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "MATH_EXPR:CRASH_TRIGGER:59"
    assert content == expected, f"Expected bug report to contain '{expected}', but found '{content}'."

def test_build_sh_modified():
    # The build script must be modified to fix the dynamic linking issue.
    # We check if LD_LIBRARY_PATH is mentioned in the build script.
    file_path = "/home/user/project/build.sh"
    assert os.path.isfile(file_path), f"Build script {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    # Checking for common ways to fix the dynamic linking in bash
    fixed = "LD_LIBRARY_PATH" in content or "-Wl,-rpath" in content or "ldconfig" in content
    assert fixed, "The build.sh script does not appear to be modified to fix the dynamic linking issue (e.g., setting LD_LIBRARY_PATH)."