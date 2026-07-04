# test_final_state.py
import os

def test_analyzer_cpp_exists_and_valid():
    path = "/home/user/analyzer.cpp"
    assert os.path.isfile(path), f"File {path} is missing. Did you create the analyzer program?"

    with open(path, "r") as f:
        content = f.read()

    assert "assert" in content, f"{path} does not contain 'assert'. You must include an assertion-based validation routine."
    assert "app.log" in content, f"{path} does not seem to read '/home/user/app.log'."

def test_solution_txt_correct():
    path = "/home/user/solution.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you write the final state to it?"

    # Compute the expected final state
    A = 17
    B = 29
    M = 999983
    for _ in range(1, 500001):
        next_A = (13 * A + 19 * B) % M
        next_B = (23 * A + 31 * B) % M
        A = next_A
        B = next_B

    expected_content = f"500000,{A},{B}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Contents of {path} are incorrect. Expected '{expected_content}', got '{content}'."