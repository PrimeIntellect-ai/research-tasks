# test_final_state.py

import os
import re
import stat
import pytest

def test_sorted_versions_log():
    log_path = "/home/user/sorted_versions.log"
    assert os.path.isfile(log_path), f"Output file {log_path} does not exist."

    expected_lines = [
        "ORG_SYS 0.9.9",
        "ORG_SYS 1.2.3",
        "ORG_SYS 1.2.14",
        "ORG_SYS 1.10.1",
        "ORG_SYS 2.0.0",
        "ORG_SYS 2.1.0",
        "ORG_SYS 2.10.0",
        "ORG_SYS 10.0.0",
        "ORG_SYS 10.0.1"
    ]

    with open(log_path, "r") as f:
        content = f.read()

    lines = content.strip().split('\n')
    assert lines == expected_lines, f"The content of {log_path} does not match the expected sorted output."

def test_sorter_cpp_constraints():
    cpp_path = "/home/user/sorter.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        code = f.read()

    # Check for forbidden standard library components
    forbidden_terms = ["<algorithm>", "std::sort", "std::set", "std::map"]
    for term in forbidden_terms:
        assert term not in code, f"Forbidden term '{term}' found in {cpp_path}."

    # Check for conditional compilation macro
    assert re.search(r'#\s*if(def|\s+defined\s*\()\s*PLATFORM_PREFIX', code), \
        f"Conditional compilation for PLATFORM_PREFIX not found in {cpp_path}."

    # Basic check for custom data structure (Node, Tree, BST, etc.)
    # We'll just look for struct or class since it's hard to predict exact names, 
    # but the prompt suggests checking for struct/class representing tree logic.
    assert re.search(r'\b(class|struct)\s+\w+', code), \
        f"No custom class or struct found in {cpp_path}."

def test_sorter_bin_executable():
    bin_path = "/home/user/sorter_bin"
    assert os.path.isfile(bin_path), f"Executable file {bin_path} does not exist."

    # Check if executable
    st = os.stat(bin_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), \
        f"File {bin_path} is not executable."