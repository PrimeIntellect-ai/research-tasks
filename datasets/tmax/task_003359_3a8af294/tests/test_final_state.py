# test_final_state.py

import os
import pytest

def test_recovered_token_file():
    token_file = "/home/user/recovered_token.txt"
    assert os.path.isfile(token_file), f"File {token_file} does not exist."

    with open(token_file, 'r') as f:
        content = f.read().strip()

    expected_token = "super_secret_production_key_9921"
    assert content == expected_token, f"Recovered token is incorrect. Expected '{expected_token}', got '{content}'."

def test_calc_cpp_fixed():
    calc_cpp_path = "/home/user/app/calc.cpp"
    assert os.path.isfile(calc_cpp_path), f"File {calc_cpp_path} does not exist."

    with open(calc_cpp_path, 'r') as f:
        content = f.read()

    # Check that the precision loss issue was fixed by changing float back to double
    assert "double accumulator" in content, "calc.cpp does not seem to have 'double accumulator'. The precision loss bug might not be fixed correctly."
    assert "float accumulator" not in content, "calc.cpp still contains 'float accumulator'. The precision loss bug is not fixed."

def test_output_file():
    output_file = "/home/user/output.txt"
    assert os.path.isfile(output_file), f"File {output_file} does not exist."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    # The expected output is the sum of ASCII values of "super_secret_production_key_9921" + 1.0
    # Sum of ascii values is 3360, plus 1.0 from the loop = 3361.00000
    expected_output = "3361.00000"
    assert content == expected_output, f"Output is incorrect. Expected '{expected_output}', got '{content}'."