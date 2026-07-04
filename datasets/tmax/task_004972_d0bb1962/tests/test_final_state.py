# test_final_state.py
import os

def test_solution_correct():
    solution_path = "/home/user/solution.txt"
    secret_path = "/home/user/secret_document.txt"

    # 1. Verify the solution file was created
    assert os.path.isfile(solution_path), f"The file {solution_path} does not exist. Your payload must write the recovered flag to this exact path."

    # 2. Verify the secret document still exists to derive the truth
    assert os.path.isfile(secret_path), f"The file {secret_path} is missing. The environment appears to be corrupted."

    # 3. Read the ground truth directly from the source
    with open(secret_path, "r") as f:
        expected_flag = f.read().strip()

    # 4. Read the student's output
    with open(solution_path, "r") as f:
        actual_flag = f.read().strip()

    # 5. Assert the contents match exactly
    assert actual_flag == expected_flag, (
        f"The content of {solution_path} is incorrect.\n"
        f"Expected: '{expected_flag}'\n"
        f"Got: '{actual_flag}'\n"
        "Ensure your payload successfully bypassed the filters and read the exact contents."
    )