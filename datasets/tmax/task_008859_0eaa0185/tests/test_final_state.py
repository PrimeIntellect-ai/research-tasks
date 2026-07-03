# test_final_state.py

import os
import json
import pytest
import importlib

def test_setup_py_fixed():
    """Test that setup.py has been updated to use RustExtension."""
    setup_py_path = "/home/user/log_parser_accel/setup.py"
    assert os.path.isfile(setup_py_path), f"{setup_py_path} is missing."

    with open(setup_py_path, "r") as f:
        content = f.read()

    assert "RustExtension" in content, "setup.py does not use RustExtension to build the Rust code."
    assert "setuptools_rust" in content, "setup.py does not import from setuptools_rust."

def test_rust_code_fixed():
    """Test that the Rust code has been fixed to use owned Strings instead of borrowed references."""
    lib_rs_path = "/home/user/log_parser_accel/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"{lib_rs_path} is missing."

    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "String" in content, "lib.rs should use owned `String` types for `level` and `message` instead of borrowed `&str`."
    assert "<'a>" not in content, "lib.rs should not have lifetime parameters on `LogEntry` anymore, as PyO3 does not support them."

def test_package_installed_and_usable():
    """Test that the log_parser_accel package is installed and exposes the Parser class."""
    try:
        import log_parser_accel
    except ImportError:
        pytest.fail("log_parser_accel is not installed or fails to import. Did you run `pip install -e .`?")

    assert hasattr(log_parser_accel, "Parser"), "The `Parser` class is not exposed by the `log_parser_accel` module."

    # Quick sanity check of the parser
    parser = log_parser_accel.Parser()
    assert parser.parse_line("BEGIN") is None
    entry = parser.parse_line("ERROR: Test")
    assert entry is not None
    assert entry.level == "ERROR"
    assert entry.message == "Test"

def test_run_parser_script_exists():
    """Test that the validation script was created."""
    script_path = "/home/user/run_parser.py"
    assert os.path.isfile(script_path), f"{script_path} is missing."

def test_release_results():
    """Test that the JSON output matches the expected parsed log entries."""
    log_path = "/home/user/server.log"
    results_path = "/home/user/release_results.json"

    assert os.path.isfile(results_path), f"{results_path} is missing. The script should generate this file."

    # Dynamically compute the expected result from the log file based on the described logic
    expected = []
    in_transaction = False
    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("BEGIN"):
                in_transaction = True
            elif line.startswith("END"):
                in_transaction = False
            elif in_transaction and ":" in line:
                parts = line.split(":", 1)
                expected.append({
                    "level": parts[0].strip(),
                    "message": parts[1].strip()
                })

    # Load the student's generated JSON
    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{results_path} does not contain valid JSON.")

    assert data == expected, f"The contents of {results_path} do not match the expected parsed logs.\nExpected: {expected}\nGot: {data}"