# test_final_state.py

import os
import re
import stat

def test_binaries_exist_and_executable():
    fibo_path = "/home/user/release/bin/fibo"
    prime_path = "/home/user/release/bin/prime"

    assert os.path.isfile(fibo_path), f"Binary {fibo_path} does not exist"
    assert os.access(fibo_path, os.X_OK), f"Binary {fibo_path} is not executable"

    assert os.path.isfile(prime_path), f"Binary {prime_path} does not exist"
    assert os.access(prime_path, os.X_OK), f"Binary {prime_path} is not executable"

def test_build_script_exists():
    path = "/home/user/release/build.py"
    assert os.path.isfile(path), f"File {path} does not exist"

def test_server_script_exists():
    path = "/home/user/release/server.py"
    assert os.path.isfile(path), f"File {path} does not exist"

def test_test_server_script_exists_and_uses_mock():
    path = "/home/user/release/test_server.py"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "patch" in content, "The test_server.py script does not use 'patch'"
    assert "subprocess.run" in content, "The test_server.py script does not mock 'subprocess.run'"

def test_test_results_exist_and_passed():
    path = "/home/user/release/test_results.txt"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    # Check that tests passed. Pytest outputs something like "2 passed" or "100%"
    assert "failed" not in content.lower() or "0 failed" in content.lower(), "test_results.txt indicates test failures"
    assert "passed" in content.lower(), "test_results.txt does not indicate passing tests"