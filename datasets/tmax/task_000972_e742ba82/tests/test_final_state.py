# test_final_state.py
import os

def test_stationary_dist_output():
    output_path = "/home/user/stationary_dist.txt"
    assert os.path.exists(output_path), f"Output file not found at {output_path}"
    assert os.path.isfile(output_path), f"{output_path} is not a file"

    with open(output_path, "r") as f:
        content = f.read()

    # Remove standard newline at the end if present
    if content.endswith('\n'):
        content = content[:-1]

    expected = "0.2222,0.3111,0.2444,0.2222"
    assert content == expected, f"Expected output '{expected}', but got '{content}'"

def test_c_program_exists():
    c_file_path = "/home/user/solve_markov.c"
    assert os.path.exists(c_file_path), f"C program file not found at {c_file_path}"
    assert os.path.isfile(c_file_path), f"{c_file_path} is not a file"