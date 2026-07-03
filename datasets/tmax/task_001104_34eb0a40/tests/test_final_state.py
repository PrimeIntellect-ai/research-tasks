# test_final_state.py

import os

def test_result_file_exists():
    file_path = '/home/user/result.txt'
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_result_value():
    file_path = '/home/user/result.txt'
    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, "The result.txt file is empty."

    try:
        # Convert to float to handle integers or floats like .0 or .00
        result_val = float(content)
    except ValueError:
        assert False, f"The content of result.txt ('{content}') is not a valid number."

    expected_val = 208966254.0
    assert result_val == expected_val, f"Expected the total sum to be {expected_val}, but got {result_val}."