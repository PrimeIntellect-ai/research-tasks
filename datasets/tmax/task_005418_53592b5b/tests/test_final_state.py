# test_final_state.py

import os
import pytest

def test_clean_index_exists_and_content():
    index_path = "/home/user/clean_index.txt"
    assert os.path.isfile(index_path), f"Expected file {index_path} does not exist."

    with open(index_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "docs/intro.md | Introduction Guide",
        "docs/api/reference.md | API Reference V2",
        "assets/logo.png | Company Logo"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {index_path} does not match expected output.\nExpected:\n{expected_lines}\nActual:\n{actual_lines}"

def test_watcher_cpp_exists_and_contains_required_functions():
    cpp_path = "/home/user/watcher.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "inotify_init" in content, "watcher.cpp does not contain 'inotify_init'."
    assert "inotify_add_watch" in content, "watcher.cpp does not contain 'inotify_add_watch'."
    assert "ifstream" in content, "watcher.cpp does not contain 'ifstream' (C++ standard file I/O)."

def test_watcher_executable_exists():
    exe_path = "/home/user/watcher"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."