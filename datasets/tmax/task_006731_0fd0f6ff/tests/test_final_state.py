# test_final_state.py

import os

def test_solution_file_exists():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"The solution file {solution_path} does not exist."
    assert os.path.isfile(solution_path), f"{solution_path} is not a regular file."

def test_solution_content():
    solution_path = "/home/user/solution.txt"
    with open(solution_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The password is known to be "melon" from the setup
    expected_password = "melon"
    actual_password = content.strip()

    assert actual_password == expected_password, f"Expected password '{expected_password}', but got '{actual_password}'."