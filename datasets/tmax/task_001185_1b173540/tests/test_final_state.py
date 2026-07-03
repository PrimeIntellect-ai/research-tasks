# test_final_state.py

import os

def test_result_file_exists():
    """Verify that the result file was generated."""
    result_path = "/home/user/math_project/result.txt"
    assert os.path.isfile(result_path), (
        f"The file {result_path} does not exist. Did you successfully build and run the executable?"
    )

def test_result_file_content():
    """Verify that the result file contains the correct calculated output."""
    result_path = "/home/user/math_project/result.txt"
    assert os.path.isfile(result_path), f"Cannot check content, {result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "150.00", (
        f"The content of {result_path} is incorrect. Expected '150.00', but got '{content}'."
    )

def test_binaries_exist():
    """Verify that the project was built."""
    so_path = "/home/user/math_project/libmathparse.so"
    main_path = "/home/user/math_project/main"

    assert os.path.isfile(so_path), f"The shared library {so_path} was not built."
    assert os.path.isfile(main_path), f"The executable {main_path} was not built."