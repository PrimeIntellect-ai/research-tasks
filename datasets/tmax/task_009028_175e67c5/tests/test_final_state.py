# test_final_state.py

import os

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "The solution file /home/user/solution.txt does not exist."

def test_solution_content():
    expected_file = "/tmp/expected_solution.txt"
    solution_file = "/home/user/solution.txt"

    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."
    assert os.path.isfile(solution_file), f"Solution file {solution_file} is missing."

    with open(expected_file, "r") as f:
        expected = f.read().strip().replace(" ", "").replace("\n", "").replace("\r", "")

    with open(solution_file, "r") as f:
        actual = f.read().strip().replace(" ", "").replace("\n", "").replace("\r", "")

    assert actual == expected, f"The content of solution.txt ({actual}) does not match the expected value ({expected})."