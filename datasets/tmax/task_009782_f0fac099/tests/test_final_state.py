# test_final_state.py
import os

def test_solution_file():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"Solution file {solution_path} does not exist."
    assert os.path.isfile(solution_path), f"{solution_path} is not a file."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    expected_content = "SYSTEM_RECOVERY_SUCCESS_9912"
    assert content == expected_content, f"Expected solution content to be '{expected_content}', but got '{content}'."