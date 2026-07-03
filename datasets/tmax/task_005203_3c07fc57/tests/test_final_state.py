# test_final_state.py

import os
import subprocess
import pytest

RECOVERED_LOG_PATH = "/home/user/recovered.log"
PARSER_C_PATH = "/home/user/parser.c"
PARSER_BIN_PATH = "/home/user/parser"
SCRIPT_PATH = "/home/user/regression_test.sh"

EXPECTED_LOG_CONTENT = "IP: 192.168.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1.1 USER: admin\n"

def test_recovered_log_content():
    """Verify the contents of the recovered log file."""
    assert os.path.exists(RECOVERED_LOG_PATH), f"Recovered log not found at {RECOVERED_LOG_PATH}"
    with open(RECOVERED_LOG_PATH, "r") as f:
        content = f.read()
    assert content == EXPECTED_LOG_CONTENT, "The contents of the recovered log do not match the expected deleted data."

def test_regression_test_script():
    """Verify the regression test script exists, is executable, and runs successfully."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_parser_fixed():
    """Verify the parser compiles and does not segfault on the recovered log."""
    # Ensure parser.c exists
    assert os.path.exists(PARSER_C_PATH), f"Source file not found at {PARSER_C_PATH}"

    # Compile the parser manually to ensure we test the C code directly
    compile_result = subprocess.run(["gcc", "-o", PARSER_BIN_PATH, PARSER_C_PATH], capture_output=True, text=True)
    assert compile_result.returncode == 0, f"Compilation failed: {compile_result.stderr}"

    assert os.path.exists(PARSER_BIN_PATH), f"Compiled binary not found at {PARSER_BIN_PATH}"

    # Run the compiled parser against the recovered log
    run_result = subprocess.run([PARSER_BIN_PATH, RECOVERED_LOG_PATH], capture_output=True, text=True)
    assert run_result.returncode == 0, f"Parser crashed or failed with exit code {run_result.returncode}. It may still be vulnerable to buffer overflow."