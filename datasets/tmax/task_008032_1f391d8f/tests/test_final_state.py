# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_result_matches_reference():
    result_path = "/home/user/result.txt"
    reference_path = "/home/user/reference.txt"

    assert os.path.exists(result_path), f"{result_path} does not exist."
    assert os.path.exists(reference_path), f"{reference_path} does not exist."

    with open(result_path, "r") as f:
        result_val = f.read().strip()

    with open(reference_path, "r") as f:
        reference_val = f.read().strip()

    assert result_val == reference_val, f"Result value '{result_val}' does not match reference '{reference_val}'."

def test_verify_script():
    script_path = "/home/user/verify.sh"

    assert os.path.exists(script_path), f"{script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], capture_output=True)
    assert result.returncode == 0, f"{script_path} did not exit with code 0. Output: {result.stderr.decode()}"

def test_compiled_binary_exists():
    binary_path = "/home/user/spectroscopy_sim"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    st = os.stat(binary_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{binary_path} is not executable."