# test_final_state.py

import os
import pytest

def get_expected_tokens(log_path):
    expected_tokens = []
    with open(log_path, 'r') as f:
        for line in f:
            if "REASON=SANDBOX_VIOLATION" in line:
                parts = line.strip().split('|')
                for part in parts:
                    part = part.strip()
                    if part.startswith("TOKEN="):
                        token = part.split('=')[1].strip()
                        if len(token) == 16:
                            try:
                                # Calculate sum of hex digits
                                digit_sum = sum(int(char, 16) for char in token)
                                if digit_sum % 3 == 0:
                                    expected_tokens.append(token.lower())
                            except ValueError:
                                pass
    return expected_tokens

def test_compromised_tokens_output():
    log_path = '/home/user/security.log'
    output_path = '/home/user/compromised_tokens.txt'

    assert os.path.exists(log_path), f"The input log file {log_path} is missing."
    assert os.path.exists(output_path), f"The output file {output_path} was not created."

    expected_tokens = get_expected_tokens(log_path)

    with open(output_path, 'r') as f:
        actual_tokens = [line.strip() for line in f if line.strip()]

    assert actual_tokens == expected_tokens, (
        f"The contents of {output_path} are incorrect.\n"
        f"Expected: {expected_tokens}\n"
        f"Found: {actual_tokens}"
    )