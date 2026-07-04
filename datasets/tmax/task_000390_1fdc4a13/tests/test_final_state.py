# test_final_state.py

import os
import subprocess
import tempfile

def test_minimal_leak_file():
    path = "/home/user/minimal_leak.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip().split()

    assert content == ["837", "912"], f"Content of {path} is incorrect. Expected ['837', '912'], got {content}"

def test_test_leak_script_exists_and_executable():
    path = "/home/user/test_leak.sh"
    assert os.path.isfile(path), f"Missing script: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_test_leak_script_behavior():
    script_path = "/home/user/test_leak.sh"
    leak_file = "/home/user/minimal_leak.txt"

    # Test with the minimal leak file
    result_leak = subprocess.run([script_path, leak_file], capture_output=True)
    assert result_leak.returncode == 1, f"Expected {script_path} to exit with 1 on memory leak, but got {result_leak.returncode}"

    # Test with a clean file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as clean_file:
        clean_file.write("1\n2\n3\n")
        clean_path = clean_file.name

    try:
        result_clean = subprocess.run([script_path, clean_path], capture_output=True)
        assert result_clean.returncode == 0, f"Expected {script_path} to exit with 0 on no memory leak, but got {result_clean.returncode}"
    finally:
        os.remove(clean_path)