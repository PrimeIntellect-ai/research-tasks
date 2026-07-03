# test_final_state.py

import os
import pytest
import statistics
import base64

def test_solution_file_exists_and_correct():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"File {solution_path} does not exist. The agent must save the output here."

    # Derive the expected value from the truth data
    encoded_payload = "MTAwMDAwMDAwMC4wMDAxLDEwMDAwMDAwMDAuMDAwMiwxMDAwMDAwMDAwLjAwMDM="
    decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
    prices = [float(x) for x in decoded_payload.split(',')]

    # Compute the expected standard deviation
    expected_volatility = statistics.stdev(prices)
    expected_output = f"{expected_volatility:.6f}"

    with open(solution_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_output, f"Expected solution.txt to contain '{expected_output}', but found '{content}'."