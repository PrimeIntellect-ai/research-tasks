# test_final_state.py

import os
import re
import pytest

def test_redacted_payloads_log():
    """
    Verifies that /home/user/redacted_payloads.log exists and contains the correctly
    decrypted and redacted payloads from /home/user/intercepted_payloads.txt.
    """
    input_file = "/home/user/intercepted_payloads.txt"
    output_file = "/home/user/redacted_payloads.log"

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} was not generated."

    # Compute expected output
    expected_lines = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Decode hex
            try:
                raw_bytes = bytes.fromhex(line)
            except ValueError:
                pytest.fail(f"Input file contains invalid hex: {line}")

            # XOR decrypt
            decrypted_chars = [chr(b ^ 0x2B) for b in raw_bytes]
            plaintext = "".join(decrypted_chars)

            # Redact TARGET_IP, USER, PASS
            # The format is KEY:VALUE separated by |
            fields = plaintext.split('|')
            redacted_fields = []
            for field in fields:
                if ':' in field:
                    k, v = field.split(':', 1)
                    if k in ('TARGET_IP', 'USER', 'PASS'):
                        redacted_fields.append(f"{k}:[REDACTED]")
                    else:
                        redacted_fields.append(field)
                else:
                    redacted_fields.append(field)

            expected_lines.append("|".join(redacted_fields))

    # Read actual output
    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {output_file}, "
        f"but found {len(actual_lines)}."
    )

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )