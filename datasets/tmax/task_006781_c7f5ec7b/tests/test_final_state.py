# test_final_state.py
import os

def test_c_program_exists():
    c_file = '/home/user/cov_analyzer.c'
    assert os.path.exists(c_file), f"The C program {c_file} does not exist."
    assert os.path.isfile(c_file), f"{c_file} is not a file."

def test_correlated_features_output():
    out_file = '/home/user/correlated_features.txt'
    assert os.path.exists(out_file), f"The output file {out_file} does not exist."
    assert os.path.isfile(out_file), f"{out_file} is not a file."

    with open(out_file, 'r') as f:
        content = f.read().strip()

    expected_lines = ["0,3", "2,7"]
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {out_file} are incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )