# test_final_state.py

import os
import subprocess
import pytest

def test_fix_rust_py_exists():
    path = "/home/user/fix_rust.py"
    assert os.path.isfile(path), f"Expected Python script {path} does not exist."

def test_status_txt_secured():
    path = "/home/user/status.txt"
    assert os.path.isfile(path), f"Expected status file {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "SECURED", f"Expected {path} to contain 'SECURED', but found '{content}'."

def test_cargo_check_success():
    rust_dir = "/home/user/rust_server"
    assert os.path.isdir(rust_dir), f"Rust project directory {rust_dir} does not exist."

    result = subprocess.run(
        ["cargo", "check"],
        cwd=rust_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"`cargo check` failed with errors:\n{result.stderr.decode()}"

def test_rust_main_rs_modified():
    path = "/home/user/rust_server/src/main.rs"
    assert os.path.isfile(path), f"Rust file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check for Mutex usage
    assert "Mutex" in content, "The file main.rs does not contain 'Mutex', indicating the fix was not applied."
    assert "lock().unwrap()" in content or "lock().expect(" in content, "The file main.rs does not seem to acquire the mutex lock."