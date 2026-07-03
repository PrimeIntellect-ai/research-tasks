# test_final_state.py

import os
import pytest

def test_final_answer_correct():
    inputs_path = '/home/user/legacy_math/inputs.txt'
    multiplier_path = '/home/user/multiplier.conf'
    final_answer_path = '/home/user/legacy_math/final_answer.txt'

    assert os.path.isfile(inputs_path), f"File {inputs_path} is missing."
    assert os.path.isfile(multiplier_path), f"File {multiplier_path} is missing."
    assert os.path.isfile(final_answer_path), f"File {final_answer_path} is missing. Did you save the final calculated sum?"

    # Derive expected answer from the inputs and multiplier
    with open(inputs_path, 'r') as f:
        lines = f.readlines()

    total_sum = 0
    for line in lines:
        cleaned = line.strip().replace(',', '')
        if cleaned:
            try:
                val = int(cleaned)
                total_sum += val * val
            except ValueError:
                pytest.fail(f"Could not parse '{line.strip()}' as an integer after cleaning.")

    with open(multiplier_path, 'r') as f:
        multiplier_str = f.read().strip()
        try:
            multiplier = int(multiplier_str)
        except ValueError:
            pytest.fail(f"Could not parse multiplier '{multiplier_str}' as an integer.")

    expected_answer = total_sum * multiplier

    # Check the actual answer
    with open(final_answer_path, 'r') as f:
        actual_answer_str = f.read().strip()

    assert actual_answer_str.isdigit(), f"Final answer file should contain only an integer, got: '{actual_answer_str}'"
    assert int(actual_answer_str) == expected_answer, f"Expected final answer to be {expected_answer}, but got {actual_answer_str}. The script might still have a race condition or incorrect math."