# test_final_state.py
import os

def test_bootstrap_results_exists_and_correct():
    file_path = '/home/user/bootstrap_results.txt'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "Best Alpha: 1.0",
        "5th Percentile: 0.1557",
        "95th Percentile: 0.3661"
    ]

    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert len(actual_lines) == 3, f"Expected 3 lines in {file_path}, but got {len(actual_lines)}."

    assert actual_lines[0] == expected_lines[0], f"Expected line 1 to be '{expected_lines[0]}', got '{actual_lines[0]}'."
    assert actual_lines[1] == expected_lines[1], f"Expected line 2 to be '{expected_lines[1]}', got '{actual_lines[1]}'."
    assert actual_lines[2] == expected_lines[2], f"Expected line 3 to be '{expected_lines[2]}', got '{actual_lines[2]}'."