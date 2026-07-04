# test_final_state.py
import os

def test_executable_exists():
    executable_path = "/home/user/analyze_pca"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"The result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "20000.10", f"The result file {result_path} contains '{content}', but expected '20000.10'. Ensure that exactly 0.0001 was added to the diagonal elements of the covariance matrix."

def test_cpp_code_modified():
    cpp_path = "/home/user/analyze_pca.cpp"
    assert os.path.isfile(cpp_path), f"The source file {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    # Check for the regularization value in the source code
    has_regularization = "0.0001" in content or "1e-4" in content or "1E-4" in content
    assert has_regularization, "The source code does not seem to contain the regularization constant 0.0001 (or 1e-4)."