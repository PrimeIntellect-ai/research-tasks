# test_final_state.py

import os
import sys
import pytest
import importlib.util

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"The file {log_path} is missing. Did you run test_client.sh?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["17", "ERROR: Invalid input", "111"]
    assert lines == expected, f"Contents of {log_path} do not match expected output. Got {lines}, expected {expected}."

def test_fastmath_extension_installed_and_fixed():
    # Try importing fastmath
    try:
        import fastmath
    except ImportError:
        pytest.fail("The fastmath module is not installed or importable. Did you run 'pip install .'?")

    # Test collatz logic
    try:
        steps_15 = fastmath.collatz(15)
        steps_27 = fastmath.collatz(27)
    except Exception as e:
        pytest.fail(f"Calling fastmath.collatz failed with: {e}")

    assert steps_15 == 17, f"fastmath.collatz(15) returned {steps_15}, expected 17. The C extension logic bug might not be fixed."
    assert steps_27 == 111, f"fastmath.collatz(27) returned {steps_27}, expected 111."

def test_setup_py_fixed():
    setup_path = "/home/user/math_server/setup.py"
    assert os.path.isfile(setup_path), f"The file {setup_path} is missing."

    with open(setup_path, "r") as f:
        content = f.read()

    assert "ENABLE_OPT" in content, "setup.py does not seem to check for the ENABLE_OPT environment variable."
    assert "USE_OPTIMIZED" in content, "setup.py does not seem to pass the USE_OPTIMIZED macro."
    assert "websockets" in content, "setup.py does not define 'websockets' as a dependency."

def test_server_py_validation():
    server_path = "/home/user/math_server/server.py"
    assert os.path.isfile(server_path), f"The file {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    assert "ERROR: Invalid input" in content, "server.py does not contain the exact error message 'ERROR: Invalid input'."
    assert "1000000" in content, "server.py does not seem to check the upper bound of 1000000."

def test_test_client_sh_exists():
    script_path = "/home/user/test_client.sh"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."