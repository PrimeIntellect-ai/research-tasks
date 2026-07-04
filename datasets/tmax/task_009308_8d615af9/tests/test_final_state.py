# test_final_state.py
import os

def test_covar_c_fixed():
    path = "/home/user/pipeline/covar.c"
    assert os.path.isfile(path), f"File {path} is missing"
    with open(path, "r") as f:
        content = f.read()

    # Check that sum_prod is initialized to 0
    # It might be written as `double sum_prod = 0;` or `double sum_prod = 0.0;`
    # We can check that the uninitialized version is gone or that it's initialized.
    assert "double sum_prod;" not in content, "The variable sum_prod is still uninitialized in covar.c"
    assert "sum_prod = 0" in content or "sum_prod = 0.0" in content or "sum_prod=0" in content, "sum_prod is not initialized to 0 in covar.c"

def test_executable_exists():
    path = "/home/user/pipeline/covar"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the program?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_covar_matrix_output():
    path = "/home/user/pipeline/covar_matrix.txt"
    assert os.path.isfile(path), f"Output file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "2.5000 5.0000 -2.5000",
        "5.0000 10.0000 -5.0000",
        "-2.5000 -5.0000 2.5000"
    ]

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert len(actual_lines) == 3, f"Expected 3 lines of output in {path}, got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {path} is incorrect. Expected '{expected}', got '{actual}'"