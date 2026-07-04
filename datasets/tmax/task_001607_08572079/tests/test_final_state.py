# test_final_state.py
import os
import pytest

def test_path_txt_content():
    path_txt = '/home/user/path.txt'
    assert os.path.exists(path_txt), f"The file {path_txt} does not exist."
    assert os.path.isfile(path_txt), f"{path_txt} is not a file."

    expected_lines = ["Alpha", "Beta", "Zeta", "Omega"]

    with open(path_txt, 'r') as f:
        content = f.read().strip().splitlines()

    # Clean up any trailing whitespace on lines
    content = [line.strip() for line in content if line.strip()]

    assert content == expected_lines, f"Expected path {expected_lines}, but got {content} in {path_txt}."

def test_c_source_code():
    source_file = '/home/user/path_finder.c'
    assert os.path.exists(source_file), f"The C source file {source_file} does not exist."

    with open(source_file, 'r') as f:
        content = f.read()

    assert '#include <sqlite3.h>' in content or '#include<sqlite3.h>' in content or '#include "sqlite3.h"' in content, \
        f"The file {source_file} must include sqlite3.h."

    assert 'sqlite3_bind_' in content, \
        f"The file {source_file} must use parameterized queries (sqlite3_bind_* functions)."

def test_executable_exists():
    executable = '/home/user/path_finder'
    assert os.path.exists(executable), f"The executable {executable} does not exist."
    assert os.path.isfile(executable), f"{executable} is not a file."
    assert os.access(executable, os.X_OK), f"The file {executable} is not executable."