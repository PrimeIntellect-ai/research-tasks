# test_final_state.py

import os
import subprocess
import pytest

def test_status_txt_contains_ok():
    status_file = "/home/user/status.txt"
    assert os.path.isfile(status_file), f"{status_file} does not exist. Did you run your verify.sh script?"

    with open(status_file, "r") as f:
        content = f.read().strip()

    assert content == "OK", f"Expected '{status_file}' to contain exactly 'OK', but found '{content}'"

def test_util_min_binary_exists_and_size():
    binary_path = "/home/user/src/util_min"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist. Did you run 'make target_minimal'?"

    size = os.path.getsize(binary_path)
    assert size < 20480, f"Binary {binary_path} is too large: {size} bytes (expected < 20480 bytes). Did you strip it?"

def test_util_min_not_linked_to_libm():
    binary_path = "/home/user/src/util_min"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."

    result = subprocess.run(["ldd", binary_path], capture_output=True, text=True)
    # ldd might fail if not a dynamic executable, which is fine if statically linked without libm
    if result.returncode == 0:
        assert "libm.so" not in result.stdout, f"{binary_path} is dynamically linked to libm.so, which violates constraints."

def test_util_min_is_stripped():
    binary_path = "/home/user/src/util_min"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."

    result = subprocess.run(["file", binary_path], capture_output=True, text=True)
    assert "not stripped" not in result.stdout, f"{binary_path} has not been stripped of symbols."

def test_verify_sh_exists_and_executable():
    script_path = "/home/user/verify.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_minimal_build_macro_used():
    binary_path = "/home/user/src/util_min"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."

    # Run the binary and check output to ensure MINIMAL_BUILD was defined
    result = subprocess.run([binary_path], capture_output=True, text=True)
    assert "Minimal mode active." in result.stdout, "The binary does not print 'Minimal mode active.', indicating MINIMAL_BUILD was not defined during compilation."