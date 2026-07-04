# test_final_state.py
import os

def test_c_source_exists():
    """Test that the C source code file exists."""
    assert os.path.isfile("/home/user/etl_covar.c"), "C source file /home/user/etl_covar.c is missing."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/etl_covar"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_result_file_exists():
    """Test that the covariance result file exists."""
    assert os.path.isfile("/home/user/covariance_result.txt"), "Result file /home/user/covariance_result.txt is missing."

def test_covariance_result_content():
    """Test that the covariance result is exactly correct."""
    with open("/home/user/covariance_result.txt", "r") as f:
        content = f.read().strip()

    expected = "166833.500000"
    assert content == expected, f"Incorrect covariance result. Expected '{expected}', but got '{content}'."