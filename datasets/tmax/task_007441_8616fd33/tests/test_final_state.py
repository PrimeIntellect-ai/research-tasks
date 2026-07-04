# test_final_state.py

import os
import pytest

def test_check_go_patched():
    path = "/home/user/check.go"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "go worker(1, 15, &wg, ch)" in content, "check.go does not contain the patched worker(1, 15...) call."
    assert "go worker(2, 25, &wg, ch)" in content, "check.go does not contain the patched worker(2, 25...) call."
    assert "go worker(3, 35, &wg, ch)" in content, "check.go does not contain the patched worker(3, 35...) call."

def test_check_c_exists_and_uses_pthreads():
    path = "/home/user/check.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "pthread_create" in content, "check.c does not contain 'pthread_create'. You must use POSIX threads."

def test_check_bin_is_compiled_and_executable():
    path = "/home/user/check_bin"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_deploy_ready_log_content():
    path = "/home/user/deploy_ready.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "Total: 170", f"Expected 'Total: 170' in {path}, but got '{content}'"