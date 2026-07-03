# test_final_state.py

import os
import subprocess
import pytest

def test_ci_script_execution():
    """Run ci.sh and check if it succeeds and produces the shared library."""
    ci_script = "/home/user/data_parser/ci.sh"
    assert os.path.isfile(ci_script), f"CI script {ci_script} is missing."

    result = subprocess.run(["bash", ci_script], cwd="/home/user/data_parser", capture_output=True)
    assert result.returncode == 0, f"ci.sh failed with exit code {result.returncode}. stderr: {result.stderr.decode()}"

    so_file = "/home/user/data_parser/librust_parser.so"
    assert os.path.isfile(so_file), f"Shared library {so_file} was not built by the CI script."

def test_output_json_content():
    """Check that output.json contains exactly the integer 8472."""
    output_file = "/home/user/data_parser/output.json"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "8472", f"Expected output.json to contain exactly '8472', but found '{content}'"

def test_rust_memory_management():
    """Check that lib.rs contains a mechanism to free the string."""
    lib_rs = "/home/user/data_parser/src/lib.rs"
    assert os.path.isfile(lib_rs), f"Rust file {lib_rs} is missing."

    with open(lib_rs, "r") as f:
        content = f.read()

    # Look for CString::from_raw or similar mechanism to drop the pointer
    assert "from_raw" in content or "drop" in content or "CString" in content, \
        "lib.rs does not seem to contain a mechanism to free the allocated string (e.g., CString::from_raw)."

    # Also check that it returns into raw properly
    assert "into_raw" in content, "lib.rs does not seem to use into_raw() to pass ownership to C."

def test_python_memory_management():
    """Check that parser.py calls the free function."""
    parser_py = "/home/user/data_parser/parser.py"
    assert os.path.isfile(parser_py), f"Python file {parser_py} is missing."

    with open(parser_py, "r") as f:
        content = f.read()

    # The python file must call some free function from the library
    # e.g., lib.free_string(...)
    assert "lib." in content and ("free" in content or "drop" in content), \
        "parser.py does not seem to call a free function from the Rust library to prevent memory leaks."