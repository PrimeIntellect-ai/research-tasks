# test_final_state.py

import os
import re
import pytest

def test_test_result_log():
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "SUCCESS" in content, f"Expected 'SUCCESS' in {log_path}, but found: {content}"

def test_parser_patch_exists_and_valid():
    patch_path = "/home/user/pipeline/parser.patch"
    assert os.path.isfile(patch_path), f"Patch file {patch_path} does not exist"

    with open(patch_path, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, f"File {patch_path} does not appear to be a unified diff patch"
    assert "state = 3;" in content or "state = -1;" in content, f"Patch {patch_path} doesn't seem to contain the expected state change"

def test_executable_built():
    exe_path = "/home/user/pipeline/build/mobile_test"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did the build succeed?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable"

def test_parser_c_fixed():
    parser_path = "/home/user/pipeline/src/parser.c"
    assert os.path.isfile(parser_path), f"File {parser_path} does not exist"

    with open(parser_path, "r") as f:
        content = f.read()

    # The bug was: if (state == 2 && event == 3) { state = -1; return state; }
    # It should be fixed to transition to state 3.
    assert re.search(r"if\s*\(\s*state\s*==\s*2\s*&&\s*event\s*==\s*3\s*\)\s*\{\s*state\s*=\s*3\s*;", content), \
        f"File {parser_path} does not seem to have the correct state transition fix for event 3."

def test_cmakelists_fixed():
    cmake_path = "/home/user/pipeline/CMakeLists.txt"
    assert os.path.isfile(cmake_path), f"File {cmake_path} does not exist"

    with open(cmake_path, "r") as f:
        content = f.read()

    # Check if they added link directories or changed the link library to a path
    has_link_dir = "target_link_directories" in content or "link_directories" in content
    has_find_lib = "find_library" in content
    has_direct_path = "vendor/lib" in content

    assert has_link_dir or has_find_lib or has_direct_path, \
        f"CMakeLists.txt does not seem to be modified to link the vendor/lib directory properly."