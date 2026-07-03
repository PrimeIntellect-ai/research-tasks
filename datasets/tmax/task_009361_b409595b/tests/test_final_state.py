# test_final_state.py

import os

def test_final_result_file():
    """Check that the final_result.txt file exists and contains ALL_PASSED."""
    result_file = "/home/user/final_result.txt"
    assert os.path.isfile(result_file), (
        f"The file {result_file} does not exist. "
        "Did you run the test script after fixing the code?"
    )

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == "ALL_PASSED", (
        f"The content of {result_file} is '{content}', but expected 'ALL_PASSED'. "
        "The test script did not complete successfully."
    )

def test_binary_compiled():
    """Check that the ws_vm binary was compiled."""
    binary_path = "/home/user/repo/ws_vm"
    assert os.path.isfile(binary_path), (
        f"The binary {binary_path} does not exist. "
        "Did you fix the Makefile and run 'make'?"
    )
    assert os.access(binary_path, os.X_OK), (
        f"The binary {binary_path} is not executable."
    )