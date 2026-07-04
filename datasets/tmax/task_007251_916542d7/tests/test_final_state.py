# test_final_state.py

import os
import stat
import pytest

BASE_DIR = "/home/user/rust-api"
SRC_DIR = os.path.join(BASE_DIR, "src")
BIN_DIR = os.path.join(BASE_DIR, "bin")
MAIN_RS = os.path.join(SRC_DIR, "main.rs")
RATE_LIMIT_RS = os.path.join(SRC_DIR, "rate_limit.rs")
BUILD_SH = os.path.join(BASE_DIR, "build_and_run.sh")
BIN_MAIN = os.path.join(BIN_DIR, "main")
BUILD_LOG = os.path.join(BASE_DIR, "build.log")

def test_build_script_exists_and_executable():
    assert os.path.isfile(BUILD_SH), f"File {BUILD_SH} does not exist."
    st = os.stat(BUILD_SH)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {BUILD_SH} is not executable."

def test_rate_limit_rs_content():
    assert os.path.isfile(RATE_LIMIT_RS), f"File {RATE_LIMIT_RS} was not generated."
    with open(RATE_LIMIT_RS, "r") as f:
        content = f.read().strip()

    # Check that it contains the correct Rust syntax and the decoded limit (100)
    assert "pub const LIMIT: u32 = 100;" in content, f"{RATE_LIMIT_RS} does not contain the expected Rust constant definition."

def test_compiled_binary_exists_and_executable():
    assert os.path.isdir(BIN_DIR), f"Directory {BIN_DIR} was not created."
    assert os.path.isfile(BIN_MAIN), f"Compiled binary {BIN_MAIN} does not exist."
    st = os.stat(BIN_MAIN)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled binary {BIN_MAIN} is not executable."

def test_build_log_content():
    assert os.path.isfile(BUILD_LOG), f"File {BUILD_LOG} was not generated."
    with open(BUILD_LOG, "r") as f:
        content = f.read().strip()

    expected_output = "API configured with rate limit: 100"
    assert content == expected_output, f"Expected {BUILD_LOG} to contain '{expected_output}', but got '{content}'"