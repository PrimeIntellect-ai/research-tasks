# test_final_state.py

import os
import pytest

def test_organized_directories_exist():
    modules_dir = '/home/user/organized/modules'
    docs_dir = '/home/user/organized/docs'
    assert os.path.isdir(modules_dir), f"Directory missing: {modules_dir}"
    assert os.path.isdir(docs_dir), f"Directory missing: {docs_dir}"

def test_organized_modules_contents():
    modules_dir = '/home/user/organized/modules'
    assert os.path.isdir(modules_dir), f"Directory missing: {modules_dir}"
    files = set(os.listdir(modules_dir))
    expected = {'core.dat', 'lib.dat', 'deep.dat'}
    assert files == expected, f"Expected {expected} in {modules_dir}, but found {files}"

def test_organized_docs_contents():
    docs_dir = '/home/user/organized/docs'
    assert os.path.isdir(docs_dir), f"Directory missing: {docs_dir}"
    files = set(os.listdir(docs_dir))
    expected = {'readme.txt', 'notes.md'}
    assert files == expected, f"Expected {expected} in {docs_dir}, but found {files}"

def test_sort_log_contents():
    log_file = '/home/user/sort.log'
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, 'r') as f:
        log_lines = set(line.strip() for line in f if line.strip())

    expected_lines = {
        "[SUCCESS] Moved core.dat to /home/user/organized/modules",
        "[SUCCESS] Moved lib.dat to /home/user/organized/modules",
        "[SUCCESS] Moved deep.dat to /home/user/organized/modules",
        "[SUCCESS] Moved readme.txt to /home/user/organized/docs",
        "[SUCCESS] Moved notes.md to /home/user/organized/docs"
    }

    assert log_lines == expected_lines, f"Log file contents do not match expected output. Found: {log_lines}"

def test_cpp_files_exist():
    cpp_file = '/home/user/sorter.cpp'
    executable = '/home/user/sorter'
    assert os.path.isfile(cpp_file), f"C++ source file missing: {cpp_file}"
    assert os.path.isfile(executable), f"Executable missing: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"