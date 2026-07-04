# test_final_state.py
import os

def test_parsed_logs():
    parsed_logs_path = '/home/user/parsed_logs.txt'
    input_log_path = '/home/user/project/input.log'
    binary_path = '/home/user/project/build/parser'

    assert os.path.exists(binary_path), f"The compiled parser binary is missing at {binary_path}."
    assert os.path.exists(parsed_logs_path), f"Expected output file {parsed_logs_path} does not exist."
    assert os.path.exists(input_log_path), f"Input log file {input_log_path} does not exist."

    # Derive expected output directly from the input log
    expected_lines = []
    with open(input_log_path, 'r') as f:
        for line in f:
            if line.startswith('[OK] '):
                # The C++ code uses line.substr(5), so we strip the first 5 characters
                expected_lines.append(line[5:].strip())

    expected_lines.sort()

    # Read actual output
    with open(parsed_logs_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {parsed_logs_path} do not match the expected sorted parsed logs.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )