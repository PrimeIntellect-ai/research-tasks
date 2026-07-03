# test_final_state.py
import os
import subprocess
import pytest

def test_verify_script_exists_and_executable():
    path = "/home/user/verify.sh"
    assert os.path.isfile(path), f"Missing required file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_dropper_script_exists_and_executable():
    path = "/home/user/dropper.sh"
    assert os.path.isfile(path), f"Missing required file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_verify_script_execution():
    # Run the verify script and check the exit code
    path = "/home/user/verify.sh"
    try:
        result = subprocess.run([path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"verify.sh failed with exit code {result.returncode}. STDOUT: {result.stdout} STDERR: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("verify.sh execution timed out.")
    except Exception as e:
        pytest.fail(f"Failed to execute verify.sh: {e}")

def test_payload_bin_exists():
    path = "/home/user/payload.bin"
    assert os.path.isfile(path), f"Missing required file: {path}. The dropper.sh script should have created it."