# test_final_state.py

import os
import stat
import pytest

def test_generator_cpp_exists():
    path = "/home/user/rust_app/generator.cpp"
    assert os.path.isfile(path), f"C++ source file {path} is missing."

def test_ci_pipeline_sh_exists_and_executable():
    path = "/home/user/rust_app/ci_pipeline.sh"
    assert os.path.isfile(path), f"Bash script {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {path} is not executable."

def test_generator_executable_exists():
    path = "/home/user/rust_app/generator"
    assert os.path.isfile(path), f"Compiled C++ executable {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled file {path} is not executable."

def test_generated_config_rs_content():
    path = "/home/user/rust_app/src/generated_config.rs"
    assert os.path.isfile(path), f"Generated Rust config file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "pub const BUFFER_SIZE: i32 = 1024;",
        "pub const MAX_RETRIES: i32 = 18;",
        "pub const TIMEOUT: i32 = 10;",
        "pub const WORKERS: i32 = 5;"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected sorted output. Got: {lines}"

def test_config_diff_txt_content():
    path = "/home/user/rust_app/config_diff.txt"
    assert os.path.isfile(path), f"Diff file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "+ TIMEOUT=10",
        "+ WORKERS=5",
        "~ BUFFER_SIZE=512->1024"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected sorted diff. Got: {lines}"

def test_rust_app_compiled():
    path = "/home/user/rust_app/target/debug/rust_app"
    assert os.path.isfile(path), f"Rust application executable {path} is missing. Did 'cargo build' succeed?"