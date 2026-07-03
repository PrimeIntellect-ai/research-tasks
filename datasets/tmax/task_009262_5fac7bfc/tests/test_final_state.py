# test_final_state.py
import os

def test_recovered_token_exists_and_correct():
    token_file = "/home/user/metric_app/recovered_token.txt"
    assert os.path.isfile(token_file), f"Expected file {token_file} does not exist."

    with open(token_file, "r") as f:
        content = f.read().strip()

    expected_token = "ops_token_99x_alpha"
    assert content == expected_token, f"Recovered token is incorrect. Expected '{expected_token}', got '{content}'."

def test_output_txt_exists_and_correct():
    output_file = "/home/user/metric_app/output.txt"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist. Ensure the script ran successfully."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "3.70",
        "0.00",
        "5000.00",
        "0.00",
        "2.50"
    ]

    assert lines == expected_lines, f"Output file contents are incorrect. Expected {expected_lines}, but got {lines}."