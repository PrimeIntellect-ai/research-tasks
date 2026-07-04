# test_final_state.py
import os
import pytest

def test_output_log_exists_and_correct():
    log_path = "/home/user/web_eval/output.log"
    assert os.path.isfile(log_path), f"Output log file {log_path} does not exist. The server must be executed and output redirected."

    with open(log_path, "r") as f:
        content = f.read().strip()

    # The expected result of "5 1 2 + 4 * + 3 -" is 14.
    # C's printf("%f") defaults to 6 decimal places.
    expected = "14.000000"
    assert content == expected, f"Expected output log to contain '{expected}', but found '{content}'."

def test_server_executable_exists():
    server_path = "/home/user/web_eval/server"
    assert os.path.isfile(server_path), f"Server executable {server_path} does not exist. The Makefile should compile it."
    assert os.access(server_path, os.X_OK), f"Server file {server_path} is not executable."

def test_rust_library_compiled():
    lib_path = "/home/user/web_eval/parser/target/release/libparser.a"
    assert os.path.isfile(lib_path), f"Rust static library {lib_path} does not exist. The Makefile should build the Rust project in release mode."