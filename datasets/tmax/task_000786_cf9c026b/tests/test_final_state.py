# test_final_state.py
import os
import stat

def test_executable_exists():
    """Check if the compiled executable exists and is executable."""
    executable_path = '/home/user/calc_e'
    assert os.path.isfile(executable_path), f"The executable {executable_path} does not exist."

    # Check if the file is executable
    st = os.stat(executable_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"The file {executable_path} is not executable."

def test_result_file_exists():
    """Check if the result file exists."""
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"The result file {result_path} does not exist."

def test_result_content():
    """Check if the result file contains the correct value of 'e'."""
    result_path = '/home/user/result.txt'
    with open(result_path, 'r') as f:
        content = f.read()

    expected_value = "2.718281828"
    assert expected_value in content, f"The file {result_path} does not contain the expected value '{expected_value}'. Found: {content.strip()}"