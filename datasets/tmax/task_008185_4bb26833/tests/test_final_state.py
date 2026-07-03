# test_final_state.py

import os
import stat

def test_compute_cov_c_exists():
    path = "/home/user/compute_cov.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_compute_cov_executable_exists():
    path = "/home/user/compute_cov"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    # Check if executable
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"File {path} is not executable."

def test_covariance_result():
    path = "/home/user/covariance_result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "-0.600", f"Expected covariance result to be '-0.600', but got '{content}'."