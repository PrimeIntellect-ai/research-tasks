# test_final_state.py

import os
import stat
import pytest

def test_prod_restored_data():
    path = "/home/user/prod/restored_data.txt"
    assert os.path.exists(path), f"File {path} does not exist. The deployment step may have failed."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "RESTORE_SUCCESS_99182", f"Content of {path} is incorrect. Expected 'RESTORE_SUCCESS_99182', got '{content}'."

def test_auto_restore_exp():
    path = "/home/user/auto_restore.exp"
    assert os.path.exists(path), f"Expect script {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read()

    assert "spawn" in content, f"Expect script {path} is missing 'spawn' command."
    assert "expect" in content, f"Expect script {path} is missing 'expect' command."
    assert "send" in content, f"Expect script {path} is missing 'send' command."

def test_deploy_restore_rs():
    path = "/home/user/deploy_restore.rs"
    assert os.path.exists(path), f"Rust source file {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read()

    assert "Command" in content, f"Rust source file {path} does not seem to use std::process::Command."

def test_deploy_restore_executable():
    path = "/home/user/deploy_restore"
    assert os.path.exists(path), f"Compiled Rust executable {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."